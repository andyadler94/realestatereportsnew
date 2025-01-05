# Real Estate Reports

A FastAPI application that generates detailed property reports using real estate data from HomeHarvest.

## Features

- Property search across multiple areas with customizable criteria
- Detailed property information including:
  - Price and price per square foot
  - Bedrooms and bathrooms
  - Square footage and lot size
  - Year built and days on market
  - HOA fees and parking information
  - High-quality property images
  - Agent and office contact details
- Mobile-responsive HTML reports
- Clean and modern report design
- Support for multiple search areas

## Installation

1. Clone the repository:
```bash
git clone https://github.com/andyadler94/realestatereportsnew.git
cd realestatereports
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```
HOMEHARVEST_API_KEY=your_api_key_here
HOMEHARVEST_API_URL=https://api.homeharvest.co
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Run a property search:
```bash
python test_search.py
```

The script will:
- Search for properties matching your criteria
- Generate an HTML report with property details
- Save the report with a timestamp in the filename

## Project Structure

```
realestatereports/
├── app/
│   ├── api/
│   │   └── properties.py
│   ├── schemas/
│   │   └── property.py
│   ├── services/
│   │   ├── homeharvest_service.py
│   │   ├── property_service.py
│   │   └── report_service.py
│   └── main.py
├── requirements.txt
└── test_search.py
```

## API Endpoints

- `GET /properties/search`: Search for properties with filters
  - Parameters:
    - `city`: City name
    - `state`: State code
    - `min_beds`: Minimum number of bedrooms
    - `min_baths`: Minimum number of bathrooms
    - `max_price`: Maximum price
    - `min_price`: Minimum price (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
