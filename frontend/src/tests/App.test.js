// App.test.js
import React from 'react';
import { render } from '@testing-library/react';
import App from '../App';

describe('<App />', () => {
  it('renders LoginScreen when user is not authenticated', () => {
    // Assuming you have a function or context to check auth status.
    // Mock it to return false (user not authenticated).
    jest.mock('./path-to-auth-context', () => ({
      useAuth: jest.fn().mockReturnValue({ isAuthenticated: false })
    }));

    const { getByTestId } = render(<App />);
    expect(getByTestId('login-screen')).toBeInTheDocument();
  });

  it('renders HomeScreen when user is authenticated', () => {
    jest.mock('./path-to-auth-context', () => ({
      useAuth: jest.fn().mockReturnValue({ isAuthenticated: true })
    }));

    const { getByTestId } = render(<App />);
    expect(getByTestId('home-screen')).toBeInTheDocument();
  });
});
