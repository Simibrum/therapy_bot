// App.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';
import { handleLogin } from '../authService';

// Mock the authService module
jest.mock('../authService');

describe('<App />', () => {
  it('renders LoginScreen when user is not authenticated', () => {
    // Assuming you have a function or context to check auth status.
    // Mock it to return false (user not authenticated)

    render(<App />);
    const loginScreen = screen.getByTestId('login-screen');
    expect(loginScreen).toBeInTheDocument();
  });

    it('should display HomeScreen after successful login', async () => {
        // Setup mock to simulate successful login
        handleLogin.mockResolvedValue('fake-jwt-token');

        render(<App />);

        // Simulate entering login details and submitting the form
        // Assuming your LoginScreen uses these placeholders or labels:
        const usernameInput = screen.getByTestId('username-input');
        const passwordInput = screen.getByTestId('password-input');
        const loginButton = screen.getByTestId('login-button');

        fireEvent.change(usernameInput, { target: { value: 'testuser' } });
        fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
        fireEvent.click(loginButton);

        // Use the asynchronous utility functions from react-testing-library to wait for elements
        const homeScreenElement = await screen.findByTestId('home-screen');

        expect(homeScreenElement).toBeInTheDocument();
    });
});
