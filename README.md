# HomeHarvest API

A RESTful API service for searching real estate listings with advanced filtering capabilities and report generation.

## Features

- Property search by location (zipcode or city/state)
- Advanced filtering:
  - Price range
  - Number of bedrooms and bathrooms
  - Property types (House, Multi-Family, Condo, Townhouse)
  - Days on market
- Multiple response formats:
  - JSON data format
  - HTML report with images
- API key authentication
- Webhook support for asynchronous responses

## API Endpoints

### GET /api/properties

Search for properties with detailed filtering.

```http
GET /api/properties?zipcode=34677&minBeds=3&maxBeds=4&minBaths=2&maxBaths=3&minPrice=400000&maxPrice=800000&propertyTypes=House,Condo&daysOnMarket=30&format=json
```

#### Query Parameters

| Parameter     | Type     | Description                                           |
|--------------|----------|-------------------------------------------------------|
| zipcode      | string   | ZIP code of the target area                           |
| city         | string   | City name (required if zipcode not provided)          |
| state        | string   | State (required if zipcode not provided)              |
| minBeds      | number   | Minimum number of bedrooms                            |
| maxBeds      | number   | Maximum number of bedrooms                            |
| minBaths     | number   | Minimum number of bathrooms                           |
| maxBaths     | number   | Maximum number of bathrooms                           |
| minPrice     | number   | Minimum price                                         |
| maxPrice     | number   | Maximum price                                         |
| propertyTypes| string   | Comma-separated list of property types                |
| daysOnMarket | number   | Number of days on market                             |
| format       | string   | Response format ('json' or 'html')                    |

#### Response Format (JSON)

```json
{
  "success": true,
  "timestamp": "2024-01-17T05:30:00.000Z",
  "query": {
    "location": "34677",
    "propertyTypes": ["House", "Condo"],
    "minPrice": 400000,
    "maxPrice": 800000,
    "minBeds": 3,
    "maxBeds": 4,
    "minBaths": 2,
    "maxBaths": 3,
    "daysOnMarket": 30
  },
  "results": {
    "total": 5,
    "properties": [
      {
        "full_street_line": "123 Main St",
        "city": "Oldsmar",
        "state": "FL",
        "zip": "34677",
        "list_price": 450000,
        "beds": 3,
        "full_baths": 2,
        "sqft": 2000,
        "year_built": 2010,
        "days_on_mls": 5,
        "description": "Beautiful home...",
        "photo_urls": ["http://..."],
        "mls_number": "T123456",
        "office_name": "Real Estate Co",
        "office_phone": "555-1234",
        "office_email": "office@example.com"
      }
    ]
  }
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/homeharvest-api.git
cd homeharvest-api
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the server:
```bash
npm start
```

## Development

Start the development server with hot reload:
```bash
npm run dev
```

## Environment Variables

| Variable    | Description           | Default               |
|-------------|--------------------|------------------------|
| PORT        | Server port        | 3001                  |
| API_KEY     | API authentication key | your-secret-api-key |
| HOMEHARVEST_DIR | Path to HomeHarvest installation | /path/to/homeharvest |

## Security

- API key authentication required for all endpoints
- CORS enabled for cross-origin requests
- Input validation and sanitization
- Error handling and logging

## Dependencies

- Node.js >= 18
- Express
- Python 3
- Poetry
- HomeHarvest library

## License

MIT License 