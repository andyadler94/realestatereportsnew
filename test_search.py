import asyncio
from app.services.homeharvest_service import HomeHarvestService
from app.services.report_service import ReportService
from datetime import datetime

async def test_search():
    # Initialize services
    homeharvest_service = HomeHarvestService()
    report_service = ReportService()
    
    # Search criteria for Miami area
    miami_areas = [
        {'city': 'Miami', 'state': 'FL'},
        {'city': 'Miami Beach', 'state': 'FL'},
        {'city': 'Coral Gables', 'state': 'FL'},
        {'city': 'North Miami', 'state': 'FL'},
        {'city': 'South Miami', 'state': 'FL'}
    ]
    
    all_properties = []
    
    # Search in each area
    for area in miami_areas:
        criteria = {
            'city': area['city'],
            'state': area['state'],
            'min_beds': 2,
            'min_baths': 3,
            'max_price': 700000
        }
        
        # Search for properties
        properties = await homeharvest_service.search_properties(criteria)
        all_properties.extend(properties)
    
    # Sort properties by price and limit to 8
    all_properties.sort(key=lambda x: x['price'])
    all_properties = all_properties[:8]
    
    if all_properties:
        # Generate report filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"property_report_{timestamp}.html"
        
        # Generate report
        await report_service.generate_html_report(
            properties=all_properties,
            filename=report_filename,
            viewer_name="John Smith"
        )
        
        print(f"\nReport generated and saved as: {report_filename}\n")
        print("=" * 50)
        
        # Display property details
        for prop in all_properties:
            print("ESSENTIAL INFORMATION:")
            print(f"Address:     {prop.get('street', 'N/A')} {prop.get('unit', '').strip()} {prop.get('city', 'N/A')} {prop.get('state', 'N/A')} {prop.get('zip', 'N/A')}")
            print(f"Price:       ${prop.get('price', 0):,.2f}")
            print(f"Bedrooms:    {prop.get('beds', 'N/A')}")
            print(f"Bathrooms:   {prop.get('baths', 'N/A')}")
            print(f"Location:    {prop.get('city', 'N/A')}, {prop.get('state', 'N/A')} {prop.get('zip', 'N/A')}")
            print(f"Images:      {len(prop.get('images', [])):,} available")
            print(f"MLS#:       {prop.get('mls', 'N/A')}\n")
            
            print("ADDITIONAL DETAILS:")
            print(f"Square Feet: {prop.get('sqft', 'N/A'):,}")
            print(f"Year Built:  {prop.get('year_built', 'N/A')}")
            print(f"Days Listed: {prop.get('days_on_mls', 'N/A')}")
            print(f"Price/SqFt:  ${prop.get('price_per_sqft', 'N/A')}")
            print(f"Lot Size:    {'N/A' if prop.get('lot_sqft') is None else f'{prop.get('lot_sqft'):,} sqft'}")
            print(f"HOA Fee:     {'N/A' if prop.get('hoa_fee') is None else f'${prop.get('hoa_fee'):,}/month'}")
            print(f"Parking:     {'N/A' if prop.get('parking_garage') is None else f'{prop.get('parking_garage')} car garage'}")
            print(f"Stories:     {'N/A' if prop.get('stories') is None else prop.get('stories')}")
            print(f"Area:        {prop.get('neighborhoods', 'N/A')}")
            print(f"Listed:      {prop.get('list_date', 'N/A')}\n")
            
            print("CONTACT INFORMATION:")
            print(f"Agent:       {prop.get('agent_name', 'N/A')}")
            print(f"Office:      {prop.get('office_name', 'N/A')}\n")
            
            print("DESCRIPTION:")
            description = prop.get('description', '').strip()
            if description:
                print(description[:200] + "..." if len(description) > 200 else description)
            else:
                print("No description available")
            print("\n" + "=" * 50 + "\n")
    else:
        print("\nNo properties found matching the criteria in the Miami area.")

if __name__ == "__main__":
    asyncio.run(test_search()) 