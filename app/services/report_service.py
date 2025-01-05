from typing import List, Dict, Any
from datetime import datetime
import os

class ReportService:
    async def generate_html_report(
        self,
        properties: List[Dict[str, Any]],
        filename: str,
        viewer_name: str = "Home Buyer"
    ) -> None:
        """
        Generate an HTML report for the properties and save it to a file.
        """
        try:
            # Start HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Property Report for {viewer_name}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        background-color: #ffffff;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #2c3e50;
                        margin-bottom: 10px;
                    }}
                    .attribution {{
                        color: #7f8c8d;
                        font-size: 0.9em;
                        margin-bottom: 20px;
                    }}
                    .property {{
                        margin-bottom: 40px;
                        padding: 20px;
                        border-bottom: 1px solid #eee;
                    }}
                    .property-header {{
                        margin-bottom: 20px;
                    }}
                    .price {{
                        color: #2c3e50;
                        font-size: 1.5em;
                        font-weight: bold;
                        margin: 10px 0;
                    }}
                    .address {{
                        color: #34495e;
                        font-size: 1.2em;
                        margin-bottom: 10px;
                    }}
                    .details {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 15px;
                        margin: 15px 0;
                    }}
                    .detail-item {{
                        margin-bottom: 5px;
                    }}
                    .detail-label {{
                        font-weight: bold;
                        color: #7f8c8d;
                    }}
                    .images {{
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                        margin: 20px 0;
                    }}
                    .images img {{
                        width: 100%;
                        height: auto;
                        border-radius: 5px;
                    }}
                    .description {{
                        margin: 15px 0;
                        color: #2c3e50;
                    }}
                    @media (max-width: 768px) {{
                        body {{
                            padding: 10px;
                        }}
                        .property {{
                            padding: 15px;
                        }}
                        .details {{
                            grid-template-columns: 1fr;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Property Report for {viewer_name}</h1>
                    <div class="attribution">This report has been created by Craig Harris</div>
                </div>
            """

            # Add properties (limited to 8)
            for prop in properties[:8]:
                # Format price
                price = f"${prop['price']:,.2f}"
                
                # Calculate price per sqft
                sqft = prop.get('sqft', 0)
                price_per_sqft = f"${prop['price_per_sqft']:,.2f}" if prop.get('price_per_sqft') else "N/A"
                
                # Format address
                address = f"{prop.get('street', '')} {prop.get('unit', '')}".strip()
                location = f"{prop.get('city', '')}, {prop.get('state', '')} {prop.get('zip', '')}".strip()
                
                html_content += f"""
                <div class="property">
                    <div class="property-header">
                        <div class="price">{price}</div>
                        <div class="address">
                            {address}<br>
                            {location}
                        </div>
                    </div>
                    
                    <div class="images">
                """
                
                # Add images (up to 3)
                for img_url in prop.get('images', [])[:3]:
                    html_content += f'<img src="{img_url}" alt="Property Image">'
                
                html_content += f"""
                    </div>
                    
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">Bedrooms:</span> {prop.get('beds', 'N/A')}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Bathrooms:</span> {prop.get('baths', 'N/A')}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Square Feet:</span> {prop.get('sqft', 'N/A'):,}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Price/SqFt:</span> {price_per_sqft}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Year Built:</span> {prop.get('year_built', 'N/A')}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Days on Market:</span> {prop.get('days_on_mls', 'N/A')}
                        </div>
                """
                
                # Add optional details if available
                if prop.get('lot_sqft'):
                    html_content += f"""
                        <div class="detail-item">
                            <span class="detail-label">Lot Size:</span> {prop['lot_sqft']:,} sqft
                        </div>
                    """
                
                if prop.get('hoa_fee'):
                    html_content += f"""
                        <div class="detail-item">
                            <span class="detail-label">HOA Fee:</span> ${prop['hoa_fee']:,}/month
                        </div>
                    """
                
                if prop.get('parking_garage'):
                    html_content += f"""
                        <div class="detail-item">
                            <span class="detail-label">Parking:</span> {prop['parking_garage']} car garage
                        </div>
                    """
                
                if prop.get('stories'):
                    html_content += f"""
                        <div class="detail-item">
                            <span class="detail-label">Stories:</span> {prop['stories']}
                        </div>
                    """
                
                html_content += """
                    </div>
                """
                
                # Add description if available
                if prop.get('description'):
                    html_content += f"""
                    <div class="description">
                        {prop['description']}
                    </div>
                    """
                
                html_content += """
                </div>
                """
            
            # Close HTML
            html_content += """
            </body>
            </html>
            """
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\nReport generated and saved as: {filename}")
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            raise 