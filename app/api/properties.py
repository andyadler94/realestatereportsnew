from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional, List
from app.schemas.property import SearchRequest, PropertyList, InquiryRequest, InquiryResponse, PropertyResponse, ReportRequest, ReportResponse
from app.services.property_service import PropertyService
from app.services.report_service import ReportService
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["properties"])

@router.post("/search", response_model=List[PropertyResponse])
async def search_properties(request: SearchRequest):
    """
    Search for properties based on specified criteria.
    """
    try:
        properties = await homeharvest_service.search_properties(request.dict())
        return properties
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