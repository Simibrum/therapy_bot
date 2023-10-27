// File to define a lobby scene.
import React from 'react';
import { Container, Row, Col} from 'react-bootstrap';
import { Link } from 'react-router-dom';
import room_1 from '../images/room_1.png';

const HomeScreen = () => {
    return (
        <Container fluid style={styles.container} data-testid="home-screen">
            <Row style={styles.lobby}>
                <Col xs={4} style={styles.receptionist}>
                    Receptionist (settings)
                </Col>
                <Col xs={4} style={styles.bench}>
                    Cozy waiting bench
                </Col>
                <Col xs={4} style={styles.door}>
                    <Link to={"/session"} style={styles.door}>
                        Door (new session)
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
    navBar: {
        height: '10%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    lobby: {
        flex: 1,
        padding: '0 10%'
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
        cursor: 'pointer'
    }
};

export default HomeScreen;
