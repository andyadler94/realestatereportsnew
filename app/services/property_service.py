from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from app.schemas.property import PropertyResponse, SearchRequest
from app.services.homeharvest_service import HomeHarvestService
import uuid

class PropertyService:
    def __init__(self):
        self.homeharvest = HomeHarvestService()

    async def search_properties(
        self,
        search_request: SearchRequest
    ) -> List[PropertyResponse]:
        """Search for properties based on the search criteria."""
        min_price, max_price = search_request.price_range
        min_date = datetime.now() - timedelta(days=search_request.date_range_since_listed)
        
        if not search_request.city and not search_request.zipcode:
            raise ValueError("Either city or zipcode must be provided")

        try:
            # Fetch properties from HomeHarvest
            properties = await self.homeharvest.search_properties(
                city=search_request.city,
                zipcode=search_request.zipcode,
                min_price=min_price,
                max_price=max_price,
                property_type=search_request.property_type,
                min_date=min_date,
                max_results=search_request.max_results
            )

            # Convert to PropertyResponse objects
            property_responses = []
            for prop in properties:
                if not search_request.show_listing_link:
                    prop["listing_link"] = None
                property_responses.append(PropertyResponse(**prop))

            return property_responses

        except Exception as e:
            raise Exception(f"Error searching properties: {str(e)}")

    async def create_inquiry(
        self,
        listing_id: int,
        buyer_email: str,
        buyer_first_name: str,
        buyer_last_name: str
    ) -> dict:
        """Create a new inquiry for a property listing."""
        # In production, this would save to a database and potentially
        # trigger notifications to the listing agent
        inquiry_id = str(uuid.uuid4())
        
        # Mock successful inquiry
        return {
            "status": "success",
            "message": "Inquiry recorded successfully",
            "inquiry_id": inquiry_id
        } 