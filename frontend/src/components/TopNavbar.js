// Code for the top navigation bar
import React from 'react';
import {Navbar, Nav, Container} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSignInAlt, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

function TopNavbar({ isLoggedIn, userFirstName, onLogout }) {
    return (
        <Navbar bg="white">
            {/*<Navbar.Brand>
                {isLoggedIn ? `Session for ${userFirstName}` : 'Session'}
            </Navbar.Brand>*/}
            {isLoggedIn ? (
                <Container className="justify-content-end">
                    <Navbar.Text>
                        {isLoggedIn ? (<span>Welcome, {userFirstName}</span>) : ('') }
                    </Navbar.Text>

                    <Nav.Link onClick={onLogout} style={{ marginLeft: '20px' }}>
                        <FontAwesomeIcon icon={faSignOutAlt} /> Logout
                    </Nav.Link>
                </Container>
            ) : (
                <Container className="justify-content-end">
                    <Nav.Link href="/login">
                        <FontAwesomeIcon icon={faSignInAlt} /> Login
                    </Nav.Link>
                </Container>
            )
            }
        </Navbar>
    );
}

export default TopNavbar;
