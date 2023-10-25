import React, {useEffect, useState, useCallback} from 'react';
import HomeScreen from "./components/HomeScreen";
import LoginScreen from "./components/LoginScreen";

function App() {

    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleLogin = (username, password) => {
        // Placeholder to perform log in logic
        setIsLoggedIn(true);
    };

    // Output
    return (
        <div className="App py-5">
            {!isLoggedIn ? (
                <LoginScreen onLogin={handleLogin} />
            ) : (
                <HomeScreen />
            )}
        </div>
    );
}

export default App;
