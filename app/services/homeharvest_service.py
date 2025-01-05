import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import homeharvest as hh
import pandas as pd

class HomeHarvestService:
    async def search_properties(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for properties using HomeHarvest library.
        """
        try:
            # Create location string
            location = f"{criteria['city']}, {criteria['state']}"
            
            print(f"Searching for properties in {location}...")
            
            # Use HomeHarvest to scrape properties with all property types
            properties_df = hh.scrape_property(
                location=location,
                listing_type="for_sale",
                past_days=30,  # Last 30 days
                limit=50  # Get a good sample size
            )
            
            if properties_df.empty:
                print("No properties found.")
                return []

            # Print columns for debugging
            print("\nAvailable columns:", properties_df.columns.tolist())
            
            # Convert numeric columns
            numeric_columns = [
                'list_price', 'beds', 'full_baths', 'half_baths', 'sqft', 
                'lot_sqft', 'year_built', 'days_on_mls', 'hoa_fee', 
                'parking_garage', 'stories', 'price_per_sqft'
            ]
            
            for col in numeric_columns:
                if col in properties_df.columns:
                    properties_df[col] = pd.to_numeric(properties_df[col], errors='coerce').fillna(0)
            
            # Apply filters
            if criteria.get('min_price', 0) > 0:
                properties_df = properties_df[properties_df['list_price'] >= criteria['min_price']]
            if criteria.get('max_price'):
                properties_df = properties_df[properties_df['list_price'] <= criteria['max_price']]
            if criteria.get('min_beds'):
                properties_df = properties_df[properties_df['beds'] >= criteria['min_beds']]
            if criteria.get('min_baths'):
                total_baths = properties_df['full_baths'] + (properties_df['half_baths'] * 0.5)
                properties_df = properties_df[total_baths >= criteria['min_baths']]

            # Transform to list of dictionaries
            properties = []
            for _, row in properties_df.iterrows():
                try:
                    # Get all photos
                    photos = []
                    if pd.notna(row.get('primary_photo')):
                        photos.append(str(row['primary_photo']))
                    if pd.notna(row.get('alt_photos')):
                        if isinstance(row['alt_photos'], list):
                            photos.extend([str(p) for p in row['alt_photos']])
                        elif isinstance(row['alt_photos'], str):
                            photos.extend([p.strip() for p in row['alt_photos'].split(',')])
                    
                    # Ensure we have at least one photo
                    if not photos:
                        photos = ['https://via.placeholder.com/800x600.png?text=No+Image+Available']
                    
                    # Calculate total baths
                    total_baths = float(row['full_baths']) + (float(row['half_baths']) * 0.5)
                    
                    # Format address components
                    street = str(row.get('full_street_line', '')).strip()
                    unit = str(row.get('unit', '')).strip()
                    city = str(row.get('city', '')).strip()
                    state = str(row.get('state', '')).strip()
                    zip_code = str(row.get('zip_code', '')).strip()
                    
                    # Construct full address
                    address_parts = [p for p in [street, unit, city, state, zip_code] if p]
                    full_address = ' '.join(address_parts)
                    
                    # Calculate price per square foot
                    sqft = float(row['sqft']) if row['sqft'] > 0 else None
                    price = float(row['list_price'])
                    price_per_sqft = round(price / sqft, 2) if sqft else None
                    
                    # Format neighborhoods
                    neighborhoods = str(row.get('neighborhoods', '')).strip()
                    if not neighborhoods or neighborhoods.lower() == 'nan':
                        neighborhoods = 'Information not available'
                    
                    # Create property dictionary with complete details
                    prop = {
                        'address': full_address,
                        'street': street,
                        'unit': unit,
                        'city': city,
                        'state': state,
                        'zip': zip_code,
                        'price': price,
                        'beds': int(row['beds']),
                        'baths': total_baths,
                        'sqft': int(row['sqft']),
                        'year_built': int(row['year_built']) if row['year_built'] > 0 else None,
                        'days_on_mls': int(row['days_on_mls']),
                        'description': str(row.get('text', '')).strip(),
                        'images': photos[:3],  # Limit to 3 images
                        'mls': str(row.get('mls', '')).strip(),
                        'style': str(row.get('style', '')).strip(),
                        'office_name': str(row.get('office_name', '')).strip(),
                        'office_phone': str(row.get('office_phones', [''])[0]).strip() if isinstance(row.get('office_phones'), list) else '',
                        'office_email': str(row.get('office_email', '')).strip(),
                        'agent_name': str(row.get('agent_name', '')).strip(),
                        'lot_sqft': int(row['lot_sqft']) if row['lot_sqft'] > 0 else None,
                        'hoa_fee': int(row['hoa_fee']) if row['hoa_fee'] > 0 else None,
                        'parking_garage': int(row['parking_garage']) if row['parking_garage'] > 0 else None,
                        'stories': int(row['stories']) if row['stories'] > 0 else None,
                        'neighborhoods': neighborhoods,
                        'list_date': str(row.get('list_date', '')).strip(),
                        'price_per_sqft': price_per_sqft,
                        'property_url': str(row.get('property_url', '')).strip(),
                        'new_construction': bool(row.get('new_construction', False)),
                        'status': str(row.get('status', '')).strip()
                    }
                    
                    # Only include properties with valid addresses
                    if street and city and state and zip_code:
                        properties.append(prop)
                    else:
                        print(f"Skipping property with incomplete address: {full_address}")
                        
                except Exception as e:
                    print(f"Error processing property: {str(e)}")
                    continue

            print(f"\nFound {len(properties)} properties in {location} matching criteria:")
            print(f"Price Range: ${criteria.get('min_price', 0):,} - ${criteria.get('max_price', 'No Limit'):,}")
            print(f"Minimum: {criteria.get('min_beds', 'Any')} bedrooms, {criteria.get('min_baths', 'Any')} bathrooms\n")

            # Sort properties by price
            properties.sort(key=lambda x: x['price'])
            
            return properties
                        
        except Exception as e:
            print(f"Error searching properties: {str(e)}")
            return [] 