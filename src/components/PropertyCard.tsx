import React from 'react';
import { MapPin, Bed, Bath, Square } from 'lucide-react';
import type { Property } from '../types';

interface PropertyCardProps {
  property: Property;
}

export default function PropertyCard({ property }: PropertyCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img
        src={property.imageUrl}
        alt={property.address}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-semibold">${property.price.toLocaleString()}</h3>
          <span className="text-sm text-gray-500">
            Listed {new Date(property.listedDate).toLocaleDateString()}
          </span>
        </div>
        
        <div className="flex items-center text-gray-600 mb-2">
          <MapPin className="w-4 h-4 mr-1" />
          <p className="text-sm">{property.address}, {property.city}, {property.state}</p>
        </div>

        <div className="flex justify-between text-sm text-gray-600 mt-4">
          <div className="flex items-center">
            <Bed className="w-4 h-4 mr-1" />
            <span>{property.bedrooms} beds</span>
          </div>
          <div className="flex items-center">
            <Bath className="w-4 h-4 mr-1" />
            <span>{property.bathrooms} baths</span>
          </div>
          <div className="flex items-center">
            <Square className="w-4 h-4 mr-1" />
            <span>{property.squareFeet.toLocaleString()} sq ft</span>
          </div>
        </div>
      </div>
    </div>
  );
}