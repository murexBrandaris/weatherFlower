#!/usr/bin/env python3
"""
Local development server script.
Uses Flask's development server with hot reloading.
For production, use Docker with Gunicorn instead.
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, config, args

if __name__ == "__main__":
    print("Weather Flower Development Server")
    print("=" * 40)
    print(f"Environment: {args.env}")
    print(f"Debug mode: {config['server']['debug']}")
    print(f"Host: {config['server']['host']}")
    print(f"Port: {config['server']['port']}")
    print("=" * 40)
    print("This is the Flask development server.")
    print("For production, use Docker with Gunicorn.")
    print("=" * 40)

    # Use configuration for server settings
    app.run(
        debug=config["server"]["debug"],
        host=config["server"]["host"],
        port=config["server"]["port"],
        threaded=config["server"]["threaded"],
    )
