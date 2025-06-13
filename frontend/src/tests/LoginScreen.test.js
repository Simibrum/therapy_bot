// LoginScreen.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import LoginScreen from '../components/LoginScreen';

describe('<LoginScreen />', () => {
  it('renders correctly', () => {
    render(<LoginScreen />);
    expect(screen.getByText('Username')).toBeInTheDocument();
    expect(screen.getByText('Password')).toBeInTheDocument();
  });
});
