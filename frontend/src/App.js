import React, {useState} from 'react';
import HomeScreen from "./components/HomeScreen";
import LoginScreen from "./components/LoginScreen";
import { handleLogin } from './authService';

function App() {

    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [loginError, setLoginError] = useState(null);

    async function login(username, password) {
        try {
            const token = await handleLogin(username, password);
            localStorage.setItem('jwtToken', token);
            setIsLoggedIn(true);
        } catch (error) {
            console.error('Error during login:', error);
            setLoginError(error.message);
        }
    }

    // Output
    return (
        <div className="App py-5">
            {!isLoggedIn ? (
                <LoginScreen onLogin={login} />
            ) : (
                <HomeScreen />
            )}
            {loginError && <div className="text-danger">{loginError}</div>}
        </div>
    );
}

export default App;
