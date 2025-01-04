import React from 'react';
import { Search, DollarSign, Calendar, Home, MapPin } from 'lucide-react';
import type { SearchCriteria } from '../types';

interface SearchFormProps {
  onSearch: (criteria: SearchCriteria) => void;
}

export default function SearchForm({ onSearch }: SearchFormProps) {
  const [formData, setFormData] = React.useState<SearchCriteria>({
    location: '',
    bedrooms: 0,
    bathrooms: 0,
    minPrice: 0,
    maxPrice: 1000000,
    daysOnMarket: 7,
    propertyTypes: ['House']
  });

  const [zipCode, setZipCode] = React.useState('');
  const [city, setCity] = React.useState('');
  const [state, setState] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Combine location information
    const location = zipCode ? 
      `${zipCode}` : 
      `${city}, ${state}`.replace(/^,\s*|\s*,\s*$/, '');
    
    onSearch({
      ...formData,
      location
    });
  };

  const propertyTypeOptions = [
    { value: 'House', label: 'Single Family' },
    { value: 'Multi-Family', label: 'Multi Family' },
    { value: 'Condo', label: 'Condo' },
    { value: 'Townhouse', label: 'Townhouse' }
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-md">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Location Section */}
        <div className="space-y-2 md:col-span-2">
          <label className="block text-sm font-medium text-gray-700">Location</label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="City"
                className="w-full px-4 py-2 border rounded-md"
                value={city}
                onChange={(e) => setCity(e.target.value)}
              />
            </div>
            <div>
              <input
                type="text"
                placeholder="State"
                className="w-full px-4 py-2 border rounded-md"
                value={state}
                onChange={(e) => setState(e.target.value)}
              />
            </div>
            <div>
              <input
                type="text"
                placeholder="Zip Code"
                className="w-full px-4 py-2 border rounded-md"
                value={zipCode}
                onChange={(e) => setZipCode(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Property Type Section */}
        <div className="space-y-2 md:col-span-2">
          <label className="block text-sm font-medium text-gray-700">Property Type</label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {propertyTypeOptions.map(option => (
              <label key={option.value} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.propertyTypes.includes(option.value)}
                  onChange={(e) => {
                    const newTypes = e.target.checked
                      ? [...formData.propertyTypes, option.value]
                      : formData.propertyTypes.filter(type => type !== option.value);
                    setFormData({ ...formData, propertyTypes: newTypes });
                  }}
                  className="rounded border-gray-300 text-blue-600"
                />
                <span className="text-sm text-gray-700">{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Price Range */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Price Range</label>
          <div className="flex space-x-2">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Min Price"
                className="w-full px-4 py-2 border rounded-md"
                value={formData.minPrice === 0 ? '' : formData.minPrice}
                onChange={(e) => {
                  const value = e.target.value === '' ? 0 : parseInt(e.target.value, 10);
                  setFormData(prev => ({
                    ...prev,
                    minPrice: value
                  }));
                }}
              />
            </div>
            <div className="flex-1">
              <input
                type="text"
                placeholder="Max Price"
                className="w-full px-4 py-2 border rounded-md"
                value={formData.maxPrice === 0 ? '' : formData.maxPrice}
                onChange={(e) => {
                  const value = e.target.value === '' ? 0 : parseInt(e.target.value, 10);
                  setFormData(prev => ({
                    ...prev,
                    maxPrice: value
                  }));
                }}
              />
            </div>
          </div>
        </div>

        {/* Bedrooms & Bathrooms */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Beds & Baths</label>
          <div className="flex space-x-2">
            <div className="flex-1">
              <select
                className="w-full px-4 py-2 border rounded-md"
                value={formData.bedrooms}
                onChange={(e) => setFormData({
                  ...formData,
                  bedrooms: Number(e.target.value)
                })}
              >
                <option value={0}>Any Beds</option>
                {[1, 2, 3, 4, 5].map(num => (
                  <option key={num} value={num}>{num}+ Beds</option>
                ))}
              </select>
            </div>
            <div className="flex-1">
              <select
                className="w-full px-4 py-2 border rounded-md"
                value={formData.bathrooms}
                onChange={(e) => setFormData({
                  ...formData,
                  bathrooms: Number(e.target.value)
                })}
              >
                <option value={0}>Any Baths</option>
                {[1, 1.5, 2, 2.5, 3, 3.5, 4].map(num => (
                  <option key={num} value={num}>{num}+ Baths</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Days on Market */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Listed Within</label>
          <select
            className="w-full px-4 py-2 border rounded-md"
            value={formData.daysOnMarket}
            onChange={(e) => setFormData({
              ...formData,
              daysOnMarket: Number(e.target.value)
            })}
          >
            <option value={7}>Last 7 days</option>
            <option value={14}>Last 14 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
      >
        <Search className="w-5 h-5" />
        <span>Search Properties</span>
      </button>
    </form>
  );
}