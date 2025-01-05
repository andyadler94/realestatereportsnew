from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, constr
from decimal import Decimal
from datetime import datetime

class SearchRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    phone: Optional[str] = Field(None, description="User's phone number")
    house_request_details: Optional[str] = Field(None, description="Additional details about the house request")
    price: Decimal = Field(..., description="Target price", ge=0)
    city: Optional[str] = Field(None, description="City name")
    zipcode: Optional[str] = Field(None, description="ZIP code")
    property_type: str = Field(..., description="Type of property (e.g., Single Family, Condo)")
    date_range_since_listed: int = Field(..., description="Number of days since listing", ge=1)
    show_listing_link: bool = Field(default=False, description="Whether to show direct listing links")
    max_results: int = Field(default=10, description="Maximum number of results to return", ge=1, le=10)
    generate_report: bool = Field(default=False, description="Whether to generate a beautiful HTML/PDF report")

    @property
    def price_range(self) -> tuple[Decimal, Decimal]:
        """Returns the price range (±$50,000 from target price)"""
        return (self.price - 50000, self.price + 50000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "price": 500000,
                "city": "Austin",
                "property_type": "Single Family",
                "date_range_since_listed": 30,
                "show_listing_link": True,
                "generate_report": True
            }
        }

class PropertyBase(BaseModel):
    address: str = Field(..., description="Full street address")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State code (e.g., FL)")
    zip: str = Field(..., description="ZIP code")
    price: Decimal = Field(..., description="Listing price")
    beds: int = Field(..., description="Number of bedrooms")
    baths: float = Field(..., description="Number of bathrooms")
    property_type: str = Field(..., description="Type of property")
    date_listed: datetime = Field(..., description="Date when property was listed")
    description: Optional[str] = Field(None, description="Property description")
    images: List[str] = Field(default_factory=list, description="List of image URLs")
    mls_number: str = Field(..., description="MLS number")
    listing_link: Optional[str] = Field(None, description="Direct link to listing")
    can_inquire: bool = Field(default=True, description="Whether user can inquire about this property")

class PropertyResponse(PropertyBase):
    id: int = Field(..., description="Property ID")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PropertyList(BaseModel):
    listings: List[PropertyResponse]
    total_results: int = Field(..., description="Total number of results found")

class InquiryRequest(BaseModel):
    listing_id: int = Field(..., description="ID of the listing")
    buyer_email: EmailStr = Field(..., description="Buyer's email address")
    buyer_first_name: str = Field(..., description="Buyer's first name")
    buyer_last_name: str = Field(..., description="Buyer's last name")

    class Config:
        json_schema_extra = {
            "example": {
                "listing_id": 1,
                "buyer_email": "john.doe@example.com",
                "buyer_first_name": "John",
                "buyer_last_name": "Doe"
            }
        }

class InquiryResponse(BaseModel):
    status: str = Field(..., description="Status of the inquiry")
    message: str = Field(..., description="Response message")
    inquiry_id: str = Field(..., description="Unique identifier for the inquiry")

class ReportRequest(BaseModel):
    areas: List[SearchRequest] = Field(..., description="List of areas to search in")
    viewer_name: str = Field(..., description="Name of the person the report is for")
    max_properties: Optional[int] = Field(8, description="Maximum number of properties to include in report")

class ReportResponse(BaseModel):
    report_url: str = Field(..., description="URL or path to the generated report")
    property_count: int = Field(..., description="Number of properties included in the report")
    timestamp: str = Field(..., description="When the report was generated") 