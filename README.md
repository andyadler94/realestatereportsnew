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

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Property Search and Report Generation
- `GET /api/v1/properties/search`: Search for properties and generate a report
  - Query Parameters:
    - `city` (required): City name (e.g., "Miami")
    - `zipcode` (required): ZIP code (e.g., "33101")
    - `min_price` (optional): Minimum price (e.g., 200000)
    - `max_price` (optional): Maximum price (e.g., 700000)
    - `min_beds` (optional): Minimum number of bedrooms (e.g., 2)
    - `min_baths` (optional): Minimum number of bathrooms (e.g., 2.5)
  
  Example Request:
  ```
  GET /api/v1/properties/search?city=Miami&zipcode=33101&min_price=200000&max_price=700000&min_beds=2&min_baths=2.5
  ```

  Response:
  ```json
  [
    {
      "address": "123 Ocean Drive",
      "city": "Miami",
      "state": "FL",
      "zip": "33101",
      "price": 599000,
      "beds": 3,
      "baths": 2.5,
      "sqft": 1800,
      "year_built": 2005,
      "days_on_mls": 15,
      "description": "Beautiful oceanfront property...",
      "images": [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg"
      ],
      "mls": "ABC123",
      "office_name": "Miami Realty",
      "agent_name": "John Smith",
      "lot_sqft": 5000,
      "hoa_fee": 500,
      "parking_garage": 2,
      "stories": 1,
      "neighborhoods": "South Beach",
      "list_date": "2024-01-01",
      "price_per_sqft": 332.78
    }
  ]
  ```

  Notes:
  - The endpoint automatically generates an HTML report for the search results
  - Reports are saved in the `reports` directory with timestamps
  - Reports can be accessed at `/reports/{filename}.html`

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
