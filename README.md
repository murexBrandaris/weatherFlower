# Weather Flower App

A Flask web application that generates random weather using hex flower mechanics for tabletop RPGs.

## Features

- **Interactive Hex Flower Grid**: Click-to-navigate weather generation system
- **Multiple Climate Types**: Cool, temperate, hot climates with seasonal variations

## Local Development

### Prerequisites
- Python 3.13+
- pip
- PyYAML

### Setup
```bash
# Clone the repository
git clone https://github.com/murexBrandaris/weatherFlower.git
cd weatherFlower

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python app.py --env development
```

Open your browser to `http://localhost:5000`

### Configuration
Edit `config.yaml` to customize settings for different environments:

- **development**: Debug mode enabled, local host
- **production**: Optimized for deployment
- **testing**: Isolated testing environment

### Command Line Options
```bash
# Run in different environments
python app.py --env production
python app.py --env testing

# Use custom config file
python app.py --config my_config.yaml --env production

# Show help
python app.py --help
```

## Usage

1. **Open the application** in your browser
2. **Select climate and season** from the sidebar
3. **Generate weather** by:
   - Clicking on hex cells to set specific weather
   - Using "Random Transition" for procedural generation
   - Using "Reset" to return to bottom cell

## Deployment

### Docker
```bash
# Build container
docker build -t weather-flower-app .

# Run container
docker run -p 5000:5000 weather-flower-app
```
## Project Structure

```
weatherFlower/
├── app.py                 # Main Flask application
├── config.yaml           # Configuration file
├── hex_flower.py          # Hex flower logic
├── data_readers.py        # Data loading utilities
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── static/               # CSS, JS, and data files
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── data/            # JSON data files
│   └── icons/           # SVG icons
└── templates/           # HTML templates
    └── index.html       # Main application template
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by hex flower mechanics in tabletop RPGs
- Built with Flask and modern web technologies
- Designed for the RPG community