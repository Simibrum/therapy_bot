// Therapy Session UI
import { Container, Row, Col } from 'react-bootstrap';


const SessionScreen = () => {
    return (
        <>
            <div style={styles.compositeImage}>
                <img src="path_to_therapist_image" alt="Therapist" style={styles.therapistImage}/>
                <img src="path_to_user_image" alt="User" style={styles.userImage}/>
            </div>

            <Container fluid style={styles.chatContainer}>
                <Row>
                    <Col style={styles.therapistChat}>Therapist messages...</Col>
                    <Col style={styles.userChat}>User messages and input...</Col>
                </Row>
            </Container>
        </>
    );
}

const styles = {
    compositeImage: {
        backgroundImage: 'url(path_to_room_image)',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        position: 'relative',
        height: 'desired_height', // for example, '500px'
    },
    therapistImage: {
        position: 'absolute',
        left: 0,
        top: 0,
        width: '50%', // Or any desired value
        height: '100%',
    },
    userImage: {
        position: 'absolute',
        right: 0,
        top: 0,
        width: '50%', // Or any desired value
        height: '100%',
    },
    chatContainer: {
        marginTop: 'some_value', // Ensure this is below the composite image
    },
    therapistChat: {
        // styling for therapist chat
    },
    userChat: {
        // styling for user chat and input
    },
};

export default SessionScreen;
