import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SearchForm from '../SearchForm';

describe('SearchForm', () => {
  const mockOnSearch = jest.fn();

  beforeEach(() => {
    mockOnSearch.mockClear();
  });

  it('submits search with ZIP code', async () => {
    render(<SearchForm onSearch={mockOnSearch} />);
    
    // Fill in ZIP code
    await userEvent.type(screen.getByPlaceholderText('Zip Code'), '78701');
    
    // Click search button
    fireEvent.click(screen.getByRole('button', { name: /search properties/i }));
    
    // Check if onSearch was called with correct data
    expect(mockOnSearch).toHaveBeenCalledWith(expect.objectContaining({
      location: '78701'
    }));
  });

  it('submits search with city and state', async () => {
    render(<SearchForm onSearch={mockOnSearch} />);
    
    // Fill in city and state
    await userEvent.type(screen.getByPlaceholderText('City'), 'Austin');
    await userEvent.type(screen.getByPlaceholderText('State'), 'TX');
    
    // Click search button
    fireEvent.click(screen.getByRole('button', { name: /search properties/i }));
    
    // Check if onSearch was called with correct data
    expect(mockOnSearch).toHaveBeenCalledWith(expect.objectContaining({
      location: 'Austin, TX'
    }));
  });

  it('shows error for invalid ZIP code', async () => {
    render(<SearchForm onSearch={mockOnSearch} />);
    
    // Fill in invalid ZIP code
    await userEvent.type(screen.getByPlaceholderText('Zip Code'), '123');
    
    // Click search button
    fireEvent.click(screen.getByRole('button', { name: /search properties/i }));
    
    // Check for error message
    expect(screen.getByText('Please enter a valid ZIP code')).toBeInTheDocument();
    expect(mockOnSearch).not.toHaveBeenCalled();
  });
}); 