// App code
import React from 'react';
import {BrowserRouter as Router, Route, Routes, useNavigate} from 'react-router-dom';

import HomeScreen from "./components/HomeScreen";
import LoginScreen from "./components/LoginScreen";
import SessionScreen from './components/SessionScreen';
import TopNavbar from './components/TopNavbar';
import {useUser} from './UserContext';

function RoutesHandler() {
    const navigate = useNavigate();
    const {user} = useUser();
    const {isLoggedIn, login: contextLogin, logout: contextLogout} = user;

    async function handleLogin(username, password) {
        const success = await contextLogin(username, password);
        if (success) {
            navigate('/');
        }
    }

    function handleLogout() {
        contextLogout();
        navigate('/login');
    }

    return (
        <div className="App">
            <TopNavbar isLoggedIn={isLoggedIn} userFirstName={user.firstName} onLogout={handleLogout}/>

            <Routes>
                <Route
                    path="/login"
                    element={!isLoggedIn ? <LoginScreen onLogin={handleLogin} loginError={user.loginError}/> :
                        <HomeScreen/>}>
                </Route>
                <Route
                    path="/session"
                    element={isLoggedIn ? <SessionScreen/> :
                        <LoginScreen onLogin={handleLogin} loginError={user.loginError}/>}/>
                <Route path="/" element={isLoggedIn ? <HomeScreen/> :
                    <LoginScreen onLogin={handleLogin} loginError={user.loginError}/>}/>
            </Routes>

        </div>
    );
}

function App() {
    return (
        <Router>
            <RoutesHandler />
        </Router>
    );
}

export default App;

