import React from 'react';
import PropertyCard from './PropertyCard';
import type { Property } from '../types';

interface SearchResultsProps {
  properties: Property[];
}

export default function SearchResults({ properties }: SearchResultsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
      {properties.map((property) => (
        <PropertyCard key={property.id} property={property} />
      ))}
    </div>
  );
}