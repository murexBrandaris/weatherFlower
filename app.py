import os
import yaml
import argparse
from flask import Flask, render_template, jsonify, request, session
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


def load_config(configFile="config.yaml", environment=None):
    """Load YAML configuration with environment-specific overrides"""
    # Set default configuration
    defaultConfig = {
        "server": {"debug": True, "host": "127.0.0.1", "port": 5000, "threaded": True},
        "app": {"defaultClimate": "cool", "defaultSeason": "spring"},
        "logging": {"level": "INFO"},
    }

    try:
        if os.path.exists(configFile):
            with open(configFile, "r") as f:
                config = yaml.safe_load(f)

            # Merge with defaults
            for section, values in defaultConfig.items():
                if section not in config:
                    config[section] = {}
                for key, defaultValue in values.items():
                    config[section].setdefault(key, defaultValue)

            # Apply environment-specific overrides
            if environment and environment in config:
                envConfig = config[environment]
                for section, values in envConfig.items():
                    if section in config:
                        config[section].update(values)

            return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        print("Using default configuration...")

    return defaultConfig


# Parse command line arguments and load configuration
args = parse_args()
config = load_config(configFile=args.config, environment=args.env)

app = Flask(__name__)

# Configure sessions with environment variable fallback
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or config.get("app", {}).get(
    "secretKey", "dev-fallback-key-not-secure"
)

## Set default climate and season from config
defaultClimate = config["app"]["defaultClimate"]
defaultSeason = config["app"]["defaultSeason"]

# Get the default states from the climate data
defaultStates = get_states(defaultClimate, defaultSeason)


def get_user_hex_flower():
    """Get or create a hex flower instance for the current user session"""
    if "hexFlowerState" not in session:
        # Create new instance for this user
        session["hexFlowerState"] = {
            "currentCell": 1,  # Default starting position
            "climate": defaultClimate,
            "season": defaultSeason,
        }

    # Get current states based on user's climate/season
    userClimate = session["hexFlowerState"].get("climate", defaultClimate)
    userSeason = session["hexFlowerState"].get("season", defaultSeason)
    states = get_states(userClimate, userSeason)

    # Create hex flower instance with user's current state
    hexFlowerInst = hexFlower(states)
    hexFlowerInst.set_current_cell(session["hexFlowerState"]["currentCell"])

    return hexFlowerInst


def save_user_hex_flower_state(hexFlowerInstance):
    """Save the hex flower state to the user session"""
    if "hexFlowerState" not in session:
        session["hexFlowerState"] = {}

    session["hexFlowerState"]["currentCell"] = hexFlowerInstance.get_current_cell()
    session.modified = True


@app.route("/")
def index():
    """Render the main page with the hex flower grid"""
    return render_template("index.html")


@app.route("/api/current-state", methods=["GET"])
def get_current_state():
    """Return the current state of the hex flower"""
    hexFlowerInst = get_user_hex_flower()
    currentState = hexFlowerInst.get_current_state()
    description = get_weather_description(currentState)
    effects = get_weather_effects(currentState)

    return jsonify(
        {
            "cell": hexFlowerInst.get_current_cell(),
            "state": currentState,
            "description": description,
            "effects": effects,
            "states": hexFlowerInst.states,
        }
    )


@app.route("/api/transition", methods=["POST"])
def make_transition():
    """Make a transition"""
    hexFlowerInst = get_user_hex_flower()
    # Random transition
    direction = hexFlowerInst.random_transition()
    currentState = hexFlowerInst.get_current_state()
    description = get_weather_description(currentState)
    effects = get_weather_effects(currentState)

    # Save the updated state
    save_user_hex_flower_state(hexFlowerInst)

    return jsonify(
        {
            "cell": hexFlowerInst.get_current_cell(),
            "state": currentState,
            "direction": direction,
            "description": description,
            "effects": effects,
        }
    )


@app.route("/api/reset", methods=["POST"])
def reset_state():
    """Reset the hex flower to its default state"""
    hexFlowerInst = get_user_hex_flower()
    hexFlowerInst.reset()
    currentState = hexFlowerInst.get_current_state()
    description = get_weather_description(currentState)
    effects = get_weather_effects(currentState)

    # Save the updated state
    save_user_hex_flower_state(hexFlowerInst)

    return jsonify(
        {
            "cell": hexFlowerInst.get_current_cell(),
            "state": currentState,
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
        hexFlowerInst = get_user_hex_flower()
        state = hexFlowerInst.set_current_cell(cellId)
        description = get_weather_description(state)
        effects = get_weather_effects(state)

        # Save the updated state
        save_user_hex_flower_state(hexFlowerInst)

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
    # Get user's current climate or global default
    user_climate = session.get("hexFlowerState", {}).get("climate", defaultClimate)
    return jsonify({"climates": get_climate_names(), "defaultClimate": user_climate})


@app.route("/api/seasons", methods=["GET"])
def get_seasons():
    """Return available seasons for a climate"""
    # Get climate from query parameter or user's session
    climate = request.args.get("climate")
    if not climate:
        # Fallback to user's session or global default
        user_climate = session.get("hexFlowerState", {}).get("climate", defaultClimate)
        climate = user_climate

    # Get the climate description if it exists
    description = get_climate_description(climate)

    seasons, order = get_season_names(climate)

    # Get user's current selections
    userClimate = session.get("hexFlowerState", {}).get("climate", defaultClimate)
    userSeason = session.get("hexFlowerState", {}).get("season", defaultSeason)

    # Return user's current season if they're looking at their current climate,
    # otherwise return the first season for the requested climate
    if climate == userClimate:
        selectedSeason = userSeason
    else:
        # Return the first season in the order, or first available season
        if order and len(order) > 0:
            selectedSeason = order[0]
        elif seasons and len(seasons) > 0:
            selectedSeason = next(iter(seasons.keys()))
        else:
            selectedSeason = ""

    return jsonify(
        {
            "seasons": seasons,
            "selectedSeason": selectedSeason,
            "description": description,
            "seasonOrder": order,
        }
    )


@app.route("/api/set-weather", methods=["POST"])
def set_weather():
    """Set the weather system to a specific climate and season"""
    data = request.json
    climate = data.get("climate")
    season = data.get("season")

    if not climate or not season:
        return jsonify({"success": False, "error": "Climate and season required"})

    # Update the user's session with new climate/season
    if "hexFlowerState" not in session:
        session["hexFlowerState"] = {}

    session["hexFlowerState"]["climate"] = climate
    session["hexFlowerState"]["season"] = season
    session["hexFlowerState"]["currentCell"] = 1  # Reset to starting position
    session.modified = True

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
