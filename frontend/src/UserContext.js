// Provide UserContext to the entire app by wrapping the App component in UserContext
import React, {createContext, useContext, useState} from 'react';
import {handleLogin} from "./authService";

const UserContext = createContext();

export const useUser = () => {
    return useContext(UserContext);
};

export const UserProvider = ({ children }) => {

    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [loginError, setLoginError] = useState(null);
    const [userFirstName, setUserFirstName] = useState(null);
    const [userID, setUserID] = useState(null);
    const [userToken, setUserToken] = useState(null);

    async function login(username, password) {

        try {
            const data = await handleLogin(username, password);
            // 1. Store the JWT token in localStorage and set the token in state
            localStorage.setItem('jwtToken', data.token);
            setUserToken(data.token);
            // 2. Update the user state
            setIsLoggedIn(true);
            // 3. Update the user first name
            setUserFirstName(data.firstName);
            // 4. Update the user ID
            setUserID(data.id);

        } catch (error) {
            console.error('Error during login:', error);
            // 1. Update the error state
            setLoginError(error.message);
        }
    }

    function logout() {
        // 1. Clear the JWT token (or any other session data) from localStorage
        localStorage.removeItem('jwtToken');

        // 2. Clear the user first name
        setUserFirstName(null);

        // 3. Update the user state
        setIsLoggedIn(false);
    }

    const user = {
        isLoggedIn,
        firstName: userFirstName,
        id: userID,
        token: userToken,
        error: loginError,
        login,
        logout
    };

    const contextValue = {
        user
    };

    return (
        <UserContext.Provider value={contextValue}>
            {children}
        </UserContext.Provider>
    );
};
