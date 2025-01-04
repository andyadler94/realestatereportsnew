import express from 'express';
import { exec } from 'child_process';
import cors from 'cors';

const app = express();
const API_KEY = process.env.API_KEY || 'your-secret-api-key'; // In production, use environment variable

app.use(cors());
app.use(express.json());

// Middleware to verify API key
const verifyApiKey = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey || apiKey !== API_KEY) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  next();
};

// Path to the HomeHarvest directory
const HOMEHARVEST_DIR = '/Users/andrewshwetzer/HomeHarvest';

// GET endpoint for property search
app.get('/api/properties', verifyApiKey, async (req, res) => {
  try {
    const {
      zipcode,
      city,
      state,
      minBeds = 0,
      maxBeds,
      minBaths = 0,
      maxBaths,
      minPrice = 0,
      maxPrice = 1000000,
      propertyTypes = 'House',
      daysOnMarket = 30,
      format = 'json' // Can be 'json' or 'html'
    } = req.query;

    // Validate required parameters
    if (!zipcode && (!city || !state)) {
      return res.status(400).json({ 
        error: 'Location is required. Provide either zipcode or city and state.' 
      });
    }

    // Convert property types to array
    const propertyTypesArray = propertyTypes.split(',').map(type => type.trim());

    // Construct location string
    const location = zipcode || `${city}, ${state}`;

    const command = `
import sys
from homeharvest import scrape_property
import json

try:
    print("Starting property search...", file=sys.stderr)
    properties = scrape_property(
        location='${location}',
        listing_type='for_sale',
        property_type=${JSON.stringify(propertyTypesArray)},
        past_days=${daysOnMarket},
        include_photos=True
    )
    print(f"Found {len(properties)} properties before filtering", file=sys.stderr)
    
    # Apply all filters using AND logic
    filtered = properties[
        (properties['beds'] >= ${minBeds})
        ${maxBeds ? `& (properties['beds'] <= ${maxBeds})` : ''}
        & (properties['full_baths'] >= ${minBaths})
        ${maxBaths ? `& (properties['full_baths'] <= ${maxBaths})` : ''}
        & (properties['list_price'] >= ${minPrice})
        & (properties['list_price'] <= ${maxPrice})
    ]
    
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
`;

    exec(`cd "${HOMEHARVEST_DIR}" && poetry run python3 -c "${command.replace(/"/g, '\\"')}"`, async (error, stdout, stderr) => {
      if (stderr) {
        console.error('Command stderr:', stderr);
      }

      if (error) {
        console.error('Error executing command:', error);
        return res.status(500).json({ error: error.message, details: stderr });
      }

      try {
        const properties = JSON.parse(stdout);
        
        // Format response based on requested format
        if (format === 'html') {
          const html = generateHtmlReport(properties, {
            location,
            propertyTypes: propertyTypesArray,
            minPrice,
            maxPrice,
            minBeds,
            maxBeds,
            minBaths,
            maxBaths,
            daysOnMarket
          });
          res.setHeader('Content-Type', 'text/html');
          return res.send(html);
        }

        // Default JSON response
        const response = {
          success: true,
          timestamp: new Date().toISOString(),
          query: {
            location,
            propertyTypes: propertyTypesArray,
            minPrice,
            maxPrice,
            minBeds,
            maxBeds,
            minBaths,
            maxBaths,
            daysOnMarket
          },
          results: {
            total: properties.length,
            properties
          }
        };

        res.json(response);
      } catch (e) {
        console.error('Error parsing JSON:', e);
        console.error('Raw output:', stdout);
        res.status(500).json({ 
          error: 'Failed to parse properties data',
          details: stdout
        });
      }
    });
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Helper function to generate HTML report
function generateHtmlReport(properties, criteria) {
  return `<!DOCTYPE html>
    <html>
      <head>
        <style>
          body { font-family: "Helvetica Neue", Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
          .header { text-align: center; margin-bottom: 30px; }
          .criteria { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 30px; }
          .property-card { border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
          .property-image { width: 100%; height: 300px; object-fit: cover; border-radius: 4px; }
          .property-price { font-size: 24px; font-weight: bold; color: #2563eb; }
          .property-details { margin: 15px 0; }
          .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Property Report</h1>
          <p>Generated on ${new Date().toLocaleDateString()}</p>
        </div>

        <div class="criteria">
          <h2>Search Criteria</h2>
          <p>Location: ${criteria.location}</p>
          <p>Property Types: ${criteria.propertyTypes.join(', ')}</p>
          <p>Price Range: $${criteria.minPrice.toLocaleString()} - $${criteria.maxPrice.toLocaleString()}</p>
          <p>Bedrooms: ${criteria.minBeds}${criteria.maxBeds ? ` - ${criteria.maxBeds}` : '+'}</p>
          <p>Bathrooms: ${criteria.minBaths}${criteria.maxBaths ? ` - ${criteria.maxBaths}` : '+'}</p>
          <p>Days on Market: ${criteria.daysOnMarket}</p>
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

        <div class="footer">
          <p>Report generated by HomeHarvest</p>
        </div>
      </body>
    </html>`;
}

// Webhook endpoint for Zapier/Make.com integration
app.post('/api/webhook/search', verifyApiKey, async (req, res) => {
  try {
    const {
      location,
      propertyTypes = ['House'],
      minPrice = 0,
      maxPrice = 1000000,
      bedrooms = 0,
      bathrooms = 0,
      daysOnMarket = 30,
      webhookUrl // Optional webhook URL for asynchronous response
    } = req.body;

    if (!location) {
      return res.status(400).json({ error: 'Location is required' });
    }

    const command = `
import sys
from homeharvest import scrape_property
import json

try:
    print("Starting property search...", file=sys.stderr)
    properties = scrape_property(
        location='${location}',
        listing_type='for_sale',
        property_type=${JSON.stringify(propertyTypes)},
        past_days=${daysOnMarket},
        include_photos=True
    )
    print(f"Found {len(properties)} properties before filtering", file=sys.stderr)
    
    # Apply all filters using AND logic
    filtered = properties[
        (properties['beds'] >= ${bedrooms}) &
        (properties['full_baths'] >= ${bathrooms}) &
        (properties['list_price'] >= ${minPrice}) &
        (properties['list_price'] <= ${maxPrice})
    ]
    
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
`;

    exec(`cd "${HOMEHARVEST_DIR}" && poetry run python3 -c "${command.replace(/"/g, '\\"')}"`, async (error, stdout, stderr) => {
      if (stderr) {
        console.error('Command stderr:', stderr);
      }

      if (error) {
        console.error('Error executing command:', error);
        const response = { error: error.message, details: stderr };
        
        if (webhookUrl) {
          try {
            await fetch(webhookUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(response)
            });
          } catch (webhookError) {
            console.error('Error sending webhook response:', webhookError);
          }
        }
        
        return res.status(500).json(response);
      }

      try {
        const properties = JSON.parse(stdout);
        const response = {
          success: true,
          timestamp: new Date().toISOString(),
          query: {
            location,
            propertyTypes,
            minPrice,
            maxPrice,
            bedrooms,
            bathrooms,
            daysOnMarket
          },
          results: {
            total: properties.length,
            properties
          }
        };

        if (webhookUrl) {
          try {
            await fetch(webhookUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(response)
            });
          } catch (webhookError) {
            console.error('Error sending webhook response:', webhookError);
          }
        }

        res.json(response);
      } catch (e) {
        console.error('Error parsing JSON:', e);
        console.error('Raw output:', stdout);
        const response = { 
          error: 'Failed to parse properties data',
          details: stdout
        };

        if (webhookUrl) {
          try {
            await fetch(webhookUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(response)
            });
          } catch (webhookError) {
            console.error('Error sending webhook response:', webhookError);
          }
        }

        res.status(500).json(response);
      }
    });
  } catch (error) {
    console.error('Server error:', error);
    const response = { error: 'Internal server error' };

    if (req.body.webhookUrl) {
      try {
        await fetch(req.body.webhookUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(response)
        });
      } catch (webhookError) {
        console.error('Error sending webhook response:', webhookError);
      }
    }

    res.status(500).json(response);
  }
});

// Original search endpoint
app.post('/api/search', (req, res) => {
  const { command } = req.body;
  
  console.log('Executing command in directory:', HOMEHARVEST_DIR);
  
  exec(`cd "${HOMEHARVEST_DIR}" && poetry run python3 -c "${command.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
    if (stderr) {
      console.error('Command stderr:', stderr);
    }

    if (error) {
      console.error('Error executing command:', error);
      return res.status(500).json({ error: error.message });
    }
    
    try {
      const properties = JSON.parse(stdout);
      res.json({ properties });
    } catch (e) {
      console.error('Error parsing JSON:', e);
      console.error('Raw output:', stdout);
      res.status(500).json({ 
        error: 'Failed to parse properties data',
        details: stdout
      });
    }
  });
});

const PORT = process.env.PORT || 3001;

// Check if port is in use before starting server
const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}).on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`Port ${PORT} is already in use. Please try a different port.`);
    process.exit(1);
  } else {
    console.error('Server error:', err);
  }
}); 