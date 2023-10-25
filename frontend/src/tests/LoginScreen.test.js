// LoginScreen.test.js
import React from 'react';
import { render } from '@testing-library/react';
import LoginScreen from '../components/LoginScreen';

describe('<LoginScreen />', () => {
  it('renders correctly', () => {
    const { getByText } = render(<LoginScreen />);
    expect(getByText('Username')).toBeInTheDocument();
    expect(getByText('Password')).toBeInTheDocument();
  });
});
