from fastapi import APIRouter, HTTPException
from typing import Optional, List
from datetime import datetime
from ..schemas.property import SearchRequest, PropertyResponse, ReportResponse
from ..services.homeharvest_service import HomeHarvestService
from ..services.report_service import ReportService

router = APIRouter()
homeharvest_service = HomeHarvestService()
report_service = ReportService()

@router.get("/search", response_model=List[PropertyResponse])
async def search_properties(
    city: str,
    zipcode: str,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    min_beds: Optional[int] = None,
    min_baths: Optional[float] = None
):
    """
    Search for properties based on specified criteria.
    
    Parameters:
    - city: City name
    - zipcode: ZIP code
    - min_price: Minimum price (optional)
    - max_price: Maximum price (optional)
    - min_beds: Minimum number of bedrooms (optional)
    - min_baths: Minimum number of bathrooms (optional)
    """
    try:
        search_params = {
            "city": city,
            "zipcode": zipcode,
            "min_price": min_price,
            "max_price": max_price,
            "min_beds": min_beds,
            "min_baths": min_baths
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        
        properties = await homeharvest_service.search_properties(search_params)
        
        if not properties:
            raise HTTPException(
                status_code=404,
                detail="No properties found matching the specified criteria"
            )
        
        # Generate report filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"property_report_{timestamp}.html"
        
        # Generate report
        await report_service.generate_html_report(
            properties=properties,
            filename=report_filename,
            viewer_name="Home Buyer"
        )
        
        return properties
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a property report based on search criteria for multiple areas.
    """
    try:
        all_properties = []
        
        # Search in each area
        for area in request.areas:
            properties = await homeharvest_service.search_properties(area.dict())
            all_properties.extend(properties)
        
        # Sort properties by price and limit to max_properties
        all_properties.sort(key=lambda x: x['price'])
        all_properties = all_properties[:request.max_properties]
        
        if not all_properties:
            raise HTTPException(
                status_code=404,
                detail="No properties found matching the specified criteria"
            )
        
        # Generate report filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"property_report_{timestamp}.html"
        
        # Generate report
        await report_service.generate_html_report(
            properties=all_properties,
            filename=report_filename,
            viewer_name=request.viewer_name
        )
        
        return ReportResponse(
            report_url=f"/reports/{report_filename}",
            property_count=len(all_properties),
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inquire", response_model=InquiryResponse)
async def create_inquiry(
    inquiry: InquiryRequest,
    service: PropertyService = Depends(lambda: PropertyService())
):
    """
    Create an inquiry for a specific property listing.
    """
    try:
        result = await service.create_inquiry(
            inquiry.listing_id,
            inquiry.buyer_email,
            inquiry.buyer_first_name,
            inquiry.buyer_last_name
        )
        return InquiryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing your inquiry") 