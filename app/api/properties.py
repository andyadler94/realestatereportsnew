from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from app.schemas.property import SearchRequest, PropertyList, InquiryRequest, InquiryResponse
from app.services.property_service import PropertyService
from app.services.report_service import ReportService

router = APIRouter(prefix="/api/v1", tags=["properties"])

@router.post("/search", response_model=PropertyList, responses={
    200: {
        "content": {
            "application/json": {},
            "text/html": {}
        },
        "description": "Return either JSON data or HTML report based on generate_report parameter"
    }
})
async def search_properties(
    search_request: SearchRequest,
    service: PropertyService = Depends(lambda: PropertyService())
):
    """
    Search for properties with various filtering criteria.
    Returns either JSON data or an HTML report based on generate_report parameter.
    """
    try:
        properties = await service.search_properties(search_request)
        
        if search_request.generate_report:
            report_html = ReportService.generate_html_report(
                properties,
                search_request.model_dump()
            )
            return HTMLResponse(content=report_html, status_code=200)
        
        return PropertyList(
            listings=properties,
            total_results=len(properties)
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")

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