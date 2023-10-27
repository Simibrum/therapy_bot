// Login Screen
import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import {CardHeader} from "react-bootstrap";

const LoginScreen = ({ onLogin, loginError }) => {
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
        <Card>
            <CardHeader>Login</CardHeader>
            <Card.Body>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label>Username</Form.Label>
                        <Form.Control
                            type="username"
                            placeholder="Enter username"
                            data-testid="username-input"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Password"
                            data-testid="password-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Button variant="primary" type="submit" data-testid="login-button">
                        Submit
                    </Button>
                </Form>
            </Card.Body>
            {loginError && <div className="text-danger">{loginError}</div>}
        </Card>
    );
};

export default LoginScreen;
