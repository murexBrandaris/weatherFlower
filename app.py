import os
import yaml
import argparse
from flask import Flask, render_template, jsonify, request
from hex_flower import hexFlower
from data_readers import (
    get_climate_names,
    get_climate_description,
    get_season_names,
    get_states,
    get_weather_description,
    get_weather_effects,
)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Weather Flower App")
    parser.add_argument(
        "--env",
        "--environment",
        choices=["development", "production", "testing"],
        default="development",
        help="Environment to run in (default: development)",
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    return parser.parse_args()


def load_config(config_file="config.yaml", environment=None):
    """Load YAML configuration with environment-specific overrides"""
    # Set default configuration
    default_config = {
        "server": {"debug": True, "host": "127.0.0.1", "port": 5000, "threaded": True},
        "app": {"default_climate": "cool", "default_season": "spring"},
        "logging": {"level": "INFO"},
    }

    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)

            # Merge with defaults
            for section, values in default_config.items():
                if section not in config:
                    config[section] = {}
                for key, default_value in values.items():
                    config[section].setdefault(key, default_value)

            # Apply environment-specific overrides
            if environment and environment in config:
                env_config = config[environment]
                for section, values in env_config.items():
                    if section in config:
                        config[section].update(values)

            return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        print("Using default configuration...")

    return default_config


# Parse command line arguments and load configuration
args = parse_args()
config = load_config(config_file=args.config, environment=args.env)

app = Flask(__name__)

## Set default climate and season from config
defaultClimate = config["app"]["default_climate"]
defaultSeason = config["app"]["default_season"]

# Get the default states from the climate data
defaultStates = get_states(defaultClimate, defaultSeason)

# Create a global instance of hexFlower
hexFlowerInst = hexFlower(defaultStates)

# Track current climate and season
currentClimate = defaultClimate
currentSeason = defaultSeason


@app.route("/")
def index():
    """Render the main page with the hex flower grid"""
    return render_template("index.html")


@app.route("/api/current-state", methods=["GET"])
def get_current_state():
    """Return the current state of the hex flower"""
    current_state = hexFlowerInst.get_current_state()
    description = get_weather_description(current_state)
    effects = get_weather_effects(current_state)

    return jsonify(
        {
            "cell": hexFlowerInst.get_current_cell(),
            "state": current_state,
            "description": description,
            "effects": effects,
            "states": hexFlowerInst.states,
        }
    )


@app.route("/api/transition", methods=["POST"])
def make_transition():
    """Make a transition"""
    # Random transition
    direction = hexFlowerInst.random_transition()
    current_state = hexFlowerInst.get_current_state()
    description = get_weather_description(current_state)
    effects = get_weather_effects(current_state)

    return jsonify(
        {
            "cell": hexFlowerInst.get_current_cell(),
            "state": current_state,
            "direction": direction,
            "description": description,
            "effects": effects,
        }
    )


@app.route("/api/reset", methods=["POST"])
def reset_state():
    """Reset the hex flower to its default state"""
    hexFlowerInst.reset()
    current_state = hexFlowerInst.get_current_state()
    description = get_weather_description(current_state)
    effects = get_weather_effects(current_state)
    return jsonify(
        {
            "cell": hexFlowerInst.get_current_cell(),
            "state": current_state,
            "description": description,
            "effects": effects,
        }
    )


@app.route("/api/set-cell", methods=["POST"])
def set_cell():
    """Set the hex flower to a specific cell"""
    data = request.get_json()
    if not data or "cell" not in data:
        return jsonify({"error": "No cell ID provided"}), 400

    try:
        cellId = int(data["cell"])
        state = hexFlowerInst.set_current_cell(cellId)
        description = get_weather_description(state)
        effects = get_weather_effects(state)
        return jsonify(
            {
                "cell": cellId,
                "state": state,
                "description": description,
                "effects": effects,
            }
        )
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/climates", methods=["GET"])
def get_climates():
    """Return available climates"""
    return jsonify({"climates": get_climate_names(), "default_climate": currentClimate})


@app.route("/api/seasons", methods=["GET"])
def get_seasons():
    """Return available seasons for a climate"""
    climate = request.args.get("climate", currentClimate)

    # Get the climate description if it exists
    description = get_climate_description(climate)

    seasons, order = get_season_names(climate)

    return jsonify(
        {
            "seasons": seasons,
            "default_season": currentSeason if climate == currentClimate else "",
            "description": description,
            "seasonOrder": order,
        }
    )


@app.route("/api/set-weather", methods=["POST"])
def set_weather():
    """Set the weather system to a specific climate and season"""
    global currentClimate, currentSeason

    data = request.json
    climate = data.get("climate")
    season = data.get("season")

    if not climate or not season:
        return jsonify({"success": False, "error": "Climate and season required"})

    # Get weather states for the selected climate and season
    weatherStates = get_states(climate, season)

    # Update the hex flower with new states
    hexFlowerInst.set_states(weatherStates)
    hexFlowerInst.reset()  # Reset to initial state (usually center)

    # Update current selections
    currentClimate = climate
    currentSeason = season

    return jsonify({"success": True})


@app.route("/api/debug-info", methods=["GET"])
def get_debug_info():
    """Return debug information including whether debug mode is enabled"""
    return jsonify({"debug": config["server"]["debug"], "environment": args.env})


if __name__ == "__main__":
    # Use configuration for server settings
    app.run(
        debug=config["server"]["debug"],
        host=config["server"]["host"],
        port=config["server"]["port"],
        threaded=config["server"]["threaded"],
    )
