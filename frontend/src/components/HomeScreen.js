// File to define a lobby scene.
import React from 'react';
import room_1 from '../images/room_1.png';

const HomeScreen = () => {
    return (
        <div style={styles.container} data-testid="home-screen">
            <div style={styles.navBar}>
                Welcome, Test User!
            </div>
            <div style={styles.lobby}>
                <div style={styles.receptionist}>
                    Receptionist (settings)
                </div>
                <div style={styles.bench}>
                    Cozy waiting bench
                </div>
                <div style={styles.door} onClick={() => startNewSession()}>
                    Door (new session)
                </div>
            </div>
        </div>
    );

    function startNewSession() {
        // logic to start a new therapy session
        console.log('Starting new session...');
    }
};

const styles = {
    container: {
        backgroundImage: `url(${room_1})`,
        height: '100vh',
        width: '100vw',
        display: 'flex',
        flexDirection: 'column'
    },
    navBar: {
        height: '10%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    lobby: {
        flex: 1,
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 10%'
    },
    receptionist: {
        // style for the receptionist area
    },
    bench: {
        // style for the waiting bench area
    },
    door: {
        cursor: 'pointer',
        // style for the door area
    }
};

export default HomeScreen;
