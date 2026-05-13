import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard/Dashboard';

describe('Dashboard Component', () => {
  test('renders dashboard correctly', () => {
    render(<Dashboard />);
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });

  test('displays user statistics', () => {
    render(<Dashboard />);
    // Test statistics display
  });
});
