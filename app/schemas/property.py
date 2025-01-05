from typing import List, Optional
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    city: str = Field(..., description="City name")
    zipcode: str = Field(..., description="ZIP code")
    min_price: Optional[int] = Field(None, description="Minimum price")
    max_price: Optional[int] = Field(None, description="Maximum price")
    min_beds: Optional[int] = Field(None, description="Minimum number of bedrooms")
    min_baths: Optional[float] = Field(None, description="Minimum number of bathrooms")

class PropertyResponse(BaseModel):
    address: str
    city: str
    state: str
    zip: str
    price: float
    beds: int
    baths: float
    sqft: int
    year_built: Optional[int]
    days_on_mls: int
    description: Optional[str]
    images: List[str]
    mls: str
    office_name: Optional[str]
    agent_name: Optional[str]
    lot_sqft: Optional[int]
    hoa_fee: Optional[int]
    parking_garage: Optional[int]
    stories: Optional[int]
    neighborhoods: Optional[str]
    list_date: Optional[str]
    price_per_sqft: Optional[float]

class ReportResponse(BaseModel):
    report_url: str = Field(..., description="URL or path to the generated report")
    property_count: int = Field(..., description="Number of properties included in the report")
    timestamp: str = Field(..., description="When the report was generated") 