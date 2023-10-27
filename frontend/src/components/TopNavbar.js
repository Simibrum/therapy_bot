// Code for the top navigation bar
import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSignInAlt, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

function TopNavbar({ isLoggedIn, userFirstName, onLogout }) {
    return (
        <Navbar bg="white" expand="lg" className="fixed-top">
            <Navbar.Brand>
                {isLoggedIn ? `Session for ${userFirstName}` : 'Session'}
            </Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
                {isLoggedIn ? (
                    <>
                        <Navbar.Text>
                            Welcome, {userFirstName}
                        </Navbar.Text>
                        <Nav.Link onClick={onLogout}>
                            <FontAwesomeIcon icon={faSignOutAlt} /> Logout
                        </Nav.Link>
                    </>
                ) : (
                    <Nav.Link href="/login">
                        <FontAwesomeIcon icon={faSignInAlt} /> Login
                    </Nav.Link>
                )}
            </Navbar.Collapse>
        </Navbar>
    );
}

export default TopNavbar;
