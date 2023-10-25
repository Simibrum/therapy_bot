// Login Screen
import React, { useState } from 'react';

const LoginScreen = ({ onLogin}) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // This is where you'd normally send the data to your backend for authentication.
        // Assuming any login for this mockup is successful:
        onLogin(username, password);
        // For now, we'll just log the entered values
        console.log('Username:', username, 'Password:', password);
    };

    return (
        <div className="login-container" data-testid="login-screen">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        data-testid="username-input"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        data-testid="password-input"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" data-testid="login-button">Login</button>
            </form>
        </div>
    );
};

export default LoginScreen;
