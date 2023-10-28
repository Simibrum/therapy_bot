// Therapy Session UI
import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Message from './Message';
import MessageInput from './MessageInput';

import therapy_room_1 from '../images/therapy_room/therapy_room_1.png';


const SessionScreen = () => {
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (text) => {
        // Append user message to the chat
        setMessages([...messages, { sender: "user", text }]);

        // TODO: Send the message to the backend using WebSocket
        // After receiving a response from the backend, append the therapist's message
        // Example: setMessages([...messages, { sender: "therapist", text: "Response from backend" }]);
    };

    return (
        <>
            <div style={styles.compositeImage}>
                {/*<img src="path_to_therapist_image" alt="Therapist" style={styles.therapistImage}/>*/}
                {/*<img src="path_to_user_image" alt="User" style={styles.userImage}/>*/}
            </div>

            <Container fluid style={styles.chatContainer}>
                <Row>
                    <Col style={styles.therapistChat}>
                        {messages.map((message, index) => (
                            <Message key={index} sender={message.sender} text={message.text} />
                        ))}
                    </Col>
                    <Col style={styles.userChat}>
                        <MessageInput onSendMessage={handleSendMessage} />
                    </Col>
                </Row>
            </Container>
        </>
    );
};


const styles = {
    compositeImage: {
        backgroundImage: `url(${therapy_room_1})`,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        position: 'relative',
        height: '500px', // for example, '500px'
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
        padding: '5%'
        // styling for therapist chat
    },
    userChat: {
        padding: '5%'
        // styling for user chat and input
    },
};

export default SessionScreen;
