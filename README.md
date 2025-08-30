# Hex Flower Weather App

A Flask web application that displays a hex flower grid for randomized weather generation or other RPG systems.

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Features

- Interactive hex flower grid visualization
- Manual selection of state
- Random transitions based on probability 
- Reset functionality to return to the default state
- Visual indication of the current active cell

## Customization

You can customize the state descriptions in the `app.py` file by modifying the `DEFAULT_STATES` dictionary.

## How It Works

The application uses:
- Flask for the backend web server
- HTML, CSS, and JavaScript for the frontend visualization
- The `hexFlower.py` class for the hex flower logic

## License

This project is open source and available for use in your RPG campaigns.
