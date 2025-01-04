import { Property, SearchCriteria } from '../types';

export async function searchProperties(criteria: SearchCriteria): Promise<Property[]> {
  try {
    console.log('Searching with criteria:', criteria);

    // Execute the Python command using the Fetch API to communicate with our backend
    const response = await fetch('http://localhost:3001/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        command: `
import sys
from homeharvest import scrape_property
import json

try:
    print("Starting property search...", file=sys.stderr)
    properties = scrape_property(
        location='${criteria.location}',
        listing_type='for_sale',
        property_type=${JSON.stringify(criteria.propertyTypes)},
        past_days=${criteria.daysOnMarket || 30},
        include_photos=True
    )
    print(f"Found {len(properties)} properties before filtering", file=sys.stderr)
    
    # Apply all filters using AND logic
    filtered = properties[
        (properties['beds'] >= ${criteria.bedrooms}) &
        (properties['full_baths'] >= ${criteria.bathrooms}) &
        (properties['list_price'] >= ${criteria.minPrice}) &
        (properties['list_price'] <= ${criteria.maxPrice})
    ]
    
    print(f"Found {len(filtered)} properties after filtering:", file=sys.stderr)
    print(f"- Min Price: ${criteria.minPrice}", file=sys.stderr)
    print(f"- Max Price: ${criteria.maxPrice}", file=sys.stderr)
    print(f"- Beds: {${criteria.bedrooms}}+", file=sys.stderr)
    print(f"- Baths: {${criteria.bathrooms}}+", file=sys.stderr)
    print(f"- Days on Market: {${criteria.daysOnMarket}}", file=sys.stderr)
    print(f"- Property Types: {${JSON.stringify(criteria.propertyTypes)}}", file=sys.stderr)
    
    # Convert to dictionary and ensure photo_urls are included
    result = []
    for _, row in filtered.iterrows():
        property_dict = row.to_dict()
        if 'photo_urls' not in property_dict or not property_dict['photo_urls']:
            property_dict['photo_urls'] = []
        result.append(property_dict)
    
    print(json.dumps(result))
except Exception as e:
    print(f"Error occurred: {str(e)}", file=sys.stderr)
    print(json.dumps({'error': str(e)}), file=sys.stderr)
    sys.exit(1)
`
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server response error:', errorText);
      throw new Error(`Failed to fetch properties: ${errorText}`);
    }

    const data = await response.json();
    console.log('Received data:', data);
    
    if (!data.properties || !Array.isArray(data.properties)) {
      console.error('Invalid response format:', data);
      throw new Error('Invalid response format from server');
    }

    return data.properties;
  } catch (error) {
    console.error('Error searching properties:', error);
    throw error;
  }
}

export function generateReport(properties: Property[], agentInfo: {
  name: string;
  brokerage: string;
  phone: string;
  email: string;
}): string {
  const html = `<!DOCTYPE html>
    <html>
      <head>
        <style>
          body { font-family: "Helvetica Neue", Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
          .header { text-align: center; margin-bottom: 30px; }
          .property-card { border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
          .property-image { width: 100%; height: 300px; object-fit: cover; border-radius: 4px; }
          .property-price { font-size: 24px; font-weight: bold; color: #2563eb; }
          .property-details { margin: 15px 0; }
          .agent-info { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Property Report</h1>
          <p>Generated on ${new Date().toLocaleDateString()}</p>
        </div>

        ${properties.map(property => `
          <div class="property-card">
            ${property.photo_urls?.[0] ? `<img src="${property.photo_urls[0]}" alt="${property.full_street_line}" class="property-image">` : ''}
            <h2>${property.full_street_line}</h2>
            <p>${property.city}, ${property.state} ${property.zip}</p>
            <p class="property-price">$${property.list_price.toLocaleString()}</p>
            <div class="property-details">
              <p>${property.beds} beds • ${property.full_baths} baths • ${property.sqft.toLocaleString()} sqft</p>
              <p>Built in ${property.year_built}</p>
              <p>MLS# ${property.mls_number} • ${property.days_on_mls} days on market</p>
            </div>
            <p>${property.description}</p>
          </div>
        `).join('')}

        <div class="agent-info">
          <h3>${agentInfo.name}</h3>
          <p>${agentInfo.brokerage}</p>
          <p>${agentInfo.phone} • ${agentInfo.email}</p>
        </div>
      </body>
    </html>
  `;

  return html;
}

export function expandPriceRange(criteria: SearchCriteria, increment: number): SearchCriteria {
  return {
    ...criteria,
    maxPrice: criteria.maxPrice + increment,
    minPrice: Math.max(0, criteria.minPrice - increment)
  };
} 