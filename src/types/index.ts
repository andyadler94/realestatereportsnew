export interface SearchCriteria {
  location: string;
  bedrooms: number;
  bathrooms: number;
  minPrice: number;
  maxPrice: number;
  daysOnMarket?: number;
  propertyTypes: string[];
}

export interface Property {
  id: string;
  full_street_line: string;
  city: string;
  state: string;
  zip: string;
  list_price: number;
  beds: number;
  full_baths: number;
  sqft: number;
  year_built: number;
  days_on_mls: number;
  description: string;
  photo_urls: string[];
  mls_number: string;
  office_name: string;
  office_phone: string;
  office_email: string;
}

export interface AgentInfo {
  name: string;
  brokerage: string;
  phone: string;
  email: string;
  logo?: string;
}

export interface ReportConfig {
  frequency: number; // days
  maxResults: number;
  priceRangeIncrement: number;
  maxPriceRangeExpansion: number;
}