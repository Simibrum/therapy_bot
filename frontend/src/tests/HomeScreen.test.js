// HomeScreen.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import HomeScreen from '../components/HomeScreen';

describe('<HomeScreen />', () => {
  it('renders welcome message', () => {
    render(<HomeScreen />);
    expect(screen.getByText('Welcome, Test User!')).toBeInTheDocument();
  });
});
