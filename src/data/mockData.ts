import type { Property } from '../types';

export const mockProperties: Property[] = [
  {
    id: '1',
    address: '123 Main St',
    city: 'Austin',
    state: 'TX',
    price: 450000,
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 2000,
    listedDate: '2024-03-10',
    imageUrl: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994',
    description: 'Beautiful modern home in central Austin'
  },
  {
    id: '2',
    address: '456 Oak Lane',
    city: 'Austin',
    state: 'TX',
    price: 550000,
    bedrooms: 4,
    bathrooms: 3,
    squareFeet: 2500,
    listedDate: '2024-03-12',
    imageUrl: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
    description: 'Spacious family home with pool'
  }
];