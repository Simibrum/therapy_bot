// HomeScreen.test.js
import React from 'react';
import { render } from '@testing-library/react';
import HomeScreen from '../components/HomeScreen';

describe('<HomeScreen />', () => {
  it('renders welcome message', () => {
    const { getByText } = render(<HomeScreen />);
    expect(getByText('Welcome, Test User!')).toBeInTheDocument();
  });
});
