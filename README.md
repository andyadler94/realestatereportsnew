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
- RESTful API for automated report generation

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

## API Endpoints

### Property Search
- `GET /api/v1/properties/search`: Search for properties with filters
  - Parameters:
    - `city`: City name
    - `state`: State code
    - `min_beds`: Minimum number of bedrooms (optional)
    - `min_baths`: Minimum number of bathrooms (optional)
    - `max_price`: Maximum price (optional)
    - `min_price`: Minimum price (optional)

### Report Generation
- `POST /api/v1/properties/generate-report`: Generate a property report
  - Request Body:
    ```json
    {
      "areas": [
        {
          "city": "Miami",
          "state": "FL",
          "min_beds": 2,
          "min_baths": 2,
          "max_price": 700000
        },
        {
          "city": "Miami Beach",
          "state": "FL",
          "min_beds": 2,
          "min_baths": 2,
          "max_price": 700000
        }
      ],
      "viewer_name": "John Smith",
      "max_properties": 8
    }
    ```
  - Response:
    ```json
    {
      "report_url": "/reports/property_report_20250105_123456.html",
      "property_count": 8,
      "timestamp": "2025-01-05T12:34:56.789Z"
    }
    ```

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
├── reports/           # Generated report files
├── requirements.txt
└── test_search.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
