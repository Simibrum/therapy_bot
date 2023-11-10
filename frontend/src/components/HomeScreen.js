// File to define a lobby scene.
import React from 'react';
import {Col, Container, Row} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import room_1 from '../images/waiting_room/room_1.png';

const HomeScreen = () => {
    return (
        <Container fluid style={styles.container} data-testid="home-screen">
            <Row style={styles.lobby}>
                <Col xs={4} style={styles.receptionist}>
                </Col>
                <Col xs={4} style={styles.bench}>
                </Col>
                <Col xs={4} style={styles.door}>
                    <Link to={"/sessions"} style={{...styles.door, width: '100%', height: '100%'}}>
                    </Link>
                </Col>
            </Row>
        </Container>
    );
};

const styles = {
    container: {
        backgroundImage: `url(${room_1})`,
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center center',
        backgroundSize: 'cover',
        backgroundColor: 'white', // fallback color if image fails to load
        height: '100vh',
        width: '100vw'
    },
    lobby: {
        flex: 1,
        height: '100%',
    },
    receptionist: {
        // style for the receptionist area
    },
    bench: {
        // style for the waiting bench area
    },
    door: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        cursor: 'pointer',
        height: '100%'
    }
};

export default HomeScreen;
