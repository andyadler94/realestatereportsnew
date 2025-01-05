from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import random

class MockHomeHarvestService:
    def __init__(self):
        # Mock data for Oldsmar, FL properties
        self.properties = [
            {
                "mls_number": "T123456",
                "full_street_line": "123 Shore Dr",
                "city": "Oldsmar",
                "state": "FL",
                "zip": "34677",
                "list_price": 450000,
                "beds": 3,
                "full_baths": 2,
                "days_on_mls": 15,
                "description": "Beautiful waterfront home in Oldsmar with modern amenities. Features include updated kitchen, spacious master suite, and stunning water views.",
                "photo_urls": [
                    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9",
                    "https://images.unsplash.com/photo-1568605114967-8130f3a36994"
                ],
                "property_type": "Single Family"
            },
            {
                "mls_number": "T123457",
                "full_street_line": "456 Tampa Rd",
                "city": "Oldsmar",
                "state": "FL",
                "zip": "34677",
                "list_price": 375000,
                "beds": 4,
                "full_baths": 3,
                "days_on_mls": 7,
                "description": "Charming family home in the heart of Oldsmar. Recently renovated with new appliances, fresh paint, and updated flooring throughout.",
                "photo_urls": [
                    "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde",
                    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c"
                ],
                "property_type": "Single Family"
            },
            {
                "mls_number": "T123458",
                "full_street_line": "789 Forest Lakes Blvd",
                "city": "Oldsmar",
                "state": "FL",
                "zip": "34677",
                "list_price": 625000,
                "beds": 5,
                "full_baths": 4,
                "days_on_mls": 21,
                "description": "Luxurious estate in Forest Lakes. This stunning home features a gourmet kitchen, home theater, pool, and expansive outdoor entertainment area.",
                "photo_urls": [
                    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
                    "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b"
                ],
                "property_type": "Single Family"
            },
            {
                "mls_number": "T123459",
                "full_street_line": "321 Bayview Dr",
                "city": "Oldsmar",
                "state": "FL",
                "zip": "34677",
                "list_price": 299000,
                "beds": 2,
                "full_baths": 2,
                "days_on_mls": 3,
                "description": "Cozy waterfront condo with amazing views of Tampa Bay. Perfect for first-time buyers or as a vacation home.",
                "photo_urls": [
                    "https://images.unsplash.com/photo-1600573472550-8090b5e0745e",
                    "https://images.unsplash.com/photo-1600585154526-990dced4db0d"
                ],
                "property_type": "Condo"
            },
            {
                "mls_number": "T123460",
                "full_street_line": "555 State St",
                "city": "Oldsmar",
                "state": "FL",
                "zip": "34677",
                "list_price": 550000,
                "beds": 4,
                "full_baths": 3,
                "days_on_mls": 28,
                "description": "Spacious pool home in desirable neighborhood. Features include split floor plan, updated kitchen, large master suite, and screened lanai.",
                "photo_urls": [
                    "https://images.unsplash.com/photo-1600047509782-20d39509f26c",
                    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3"
                ],
                "property_type": "Single Family"
            }
        ]

    async def search_properties(
        self,
        city: Optional[str],
        zipcode: Optional[str],
        min_price: Decimal,
        max_price: Decimal,
        property_type: str,
        min_date: datetime,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for properties using mock data.
        """
        filtered_properties = []
        max_days = (datetime.now() - min_date).days

        for prop in self.properties:
            # Check location
            if city and prop["city"].lower() != city.lower():
                continue
            if zipcode and prop["zip"] != zipcode:
                continue

            # Check price range
            if not (min_price <= Decimal(str(prop["list_price"])) <= max_price):
                continue

            # Check property type
            if property_type.lower() != "any" and prop["property_type"].lower() != property_type.lower():
                continue

            # Check days on market
            if prop["days_on_mls"] > max_days:
                continue

            filtered_properties.append(prop)

        # Sort by price
        filtered_properties.sort(key=lambda x: x["list_price"])
        
        return filtered_properties[:max_results]

    async def get_property_images(self, mls_number: str) -> List[str]:
        """
        Get property images from mock data.
        """
        for prop in self.properties:
            if prop["mls_number"] == mls_number:
                return prop["photo_urls"]
        return [] 