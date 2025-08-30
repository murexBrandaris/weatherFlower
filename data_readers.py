import json


## Climate/Season Data
def get_climate_sets():
    # Read from json
    with open("static/data/climate_seasons.json") as f:
        climateSets = json.load(f)

    return climateSets


def get_climate_names():
    """Returns a dictionary of climate keys and their display names"""
    return {key: data["name"] for key, data in get_climate_sets().items()}


def get_season_names(climateKey):
    """Returns a dictionary of season keys and their display names for a given climate"""
    climateSets = get_climate_sets()
    if climateKey in climateSets:
        return {
            key: data["name"]
            for key, data in climateSets[climateKey]["seasons"].items()
        }, climateSets[climateKey]["seasonOrder"]
    return {}, []


def get_climate_description(climateKey):
    """Returns the description for a specific climate"""
    climateSets = get_climate_sets()
    if climateKey in climateSets:
        return climateSets[climateKey].get(
            "description", "No description available for this climate."
        )


def get_states(climateKey, seasonKey):
    """Returns the weather states for a specific climate and season"""
    climateSets = get_climate_sets()
    if climateKey in climateSets and seasonKey in climateSets[climateKey]["seasons"]:
        return {
            int(key): value
            for key, value in climateSets[climateKey]["seasons"][seasonKey][
                "states"
            ].items()
        }
    return {}


## Weather data
def get_weather_object():
    with open("static/data/weather_descriptions.json") as f:
        weatherDescriptions = json.load(f)
    return weatherDescriptions


def get_weather_description(weatherType):
    """
    Returns the descriptive text for a given weather type.
    """
    weatherData = get_weather_object().get(weatherType, {})
    if isinstance(weatherData, dict):
        return weatherData.get(
            "description", "No description available for this weather type."
        )
    else:
        # Fallback for old format if somehow still a string
        return (
            weatherData
            if weatherData
            else "No description available for this weather type."
        )


def get_weather_effects(weatherType):
    """
    Returns the mechanical effects for a given weather type.
    """
    weatherData = get_weather_object().get(weatherType, {})
    if isinstance(weatherData, dict):
        # Extract all keys except 'description'
        effects = {
            key: value for key, value in weatherData.items() if key != "description"
        }
        return effects
    return {}


def get_weather_data(weatherType):
    """
    Returns complete weather data (description + effects) for a given weather type.
    """
    weatherData = get_weather_object().get(weatherType, {})
    if isinstance(weatherData, dict):
        return weatherData
    else:
        # Fallback for old format
        return {
            "description": (
                weatherData
                if weatherData
                else "No description available for this weather type."
            )
        }
