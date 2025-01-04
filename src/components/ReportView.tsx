import React from 'react';
import { Download, Printer, Share2 } from 'lucide-react';
import type { Property, AgentInfo } from '../types';
import { generateReport } from '../utils/homeHarvest';

interface ReportViewProps {
  properties: Property[];
  agentInfo: AgentInfo;
}

export default function ReportView({ properties, agentInfo }: ReportViewProps) {
  const handleDownload = () => {
    const html = generateReport(properties, agentInfo);
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `property-report-${new Date().toISOString().split('T')[0]}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    const html = generateReport(properties, agentInfo);
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(html);
      printWindow.document.close();
      printWindow.print();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md">
      <div className="p-6 border-b">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Property Report</h2>
          <div className="flex space-x-2">
            <button
              onClick={handleDownload}
              className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600"
            >
              <Download className="w-4 h-4 mr-2" />
              Download
            </button>
            <button
              onClick={handlePrint}
              className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600"
            >
              <Printer className="w-4 h-4 mr-2" />
              Print
            </button>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="grid gap-6">
          {properties.map((property) => (
            <div key={property.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="md:col-span-1">
                  {property.photo_urls?.[0] && (
                    <img
                      src={property.photo_urls[0]}
                      alt={property.full_street_line}
                      className="w-full h-48 object-cover rounded-md"
                    />
                  )}
                </div>
                <div className="md:col-span-2">
                  <h3 className="text-lg font-semibold">{property.full_street_line}</h3>
                  <p className="text-gray-600">
                    {property.city}, {property.state} {property.zip}
                  </p>
                  <div className="mt-2 grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-2xl font-bold text-blue-600">
                        ${property.list_price.toLocaleString()}
                      </p>
                      <p className="text-sm text-gray-500">
                        ${Math.round(property.list_price / property.sqft).toLocaleString()}/sqft
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600">
                        {property.beds} beds • {property.full_baths} baths • {property.sqft.toLocaleString()} sqft
                      </p>
                      <p className="text-sm text-gray-500">Built in {property.year_built}</p>
                    </div>
                  </div>
                  <p className="mt-2 text-gray-700 line-clamp-2">{property.description}</p>
                  <div className="mt-4 flex justify-between items-center">
                    <p className="text-sm text-gray-500">
                      MLS# {property.mls_number} • {property.days_on_mls} days on market
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="p-6 bg-gray-50 rounded-b-lg">
        <div className="text-center">
          <p className="font-semibold text-gray-900">{agentInfo.name}</p>
          <p className="text-gray-600">{agentInfo.brokerage}</p>
          <p className="text-gray-600">{agentInfo.phone} • {agentInfo.email}</p>
        </div>
      </div>
    </div>
  );
} 