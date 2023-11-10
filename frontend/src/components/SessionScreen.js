// Therapy Session UI
import React, {useCallback, useEffect, useState} from 'react';
import {Col, Container, Row} from 'react-bootstrap';
import {useParams} from 'react-router-dom';
import Message from './Message';
import MessageInput from './MessageInput';
import {useUser} from '../UserContext';
import {websocketURL} from "../config";

import therapy_room_1 from '../images/therapy_room/therapy_room_1.png';


const SessionScreen = () => {
    // Get the session ID from the URL
    const {sessionID} = useParams();
    const {user} = useUser(); // Retrieve user information and token from context

    const [webSocket, setWebSocket] = useState(null);
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (text) => {
        // Append user message to the chat
        setMessages([...messages, {sender: "user", text}]);
        // Send to backend
        if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(JSON.stringify({message: text}));
        }
        // TODO: Send the message to the backend using WebSocket
        // After receiving a response from the backend, append the therapist's message
        // Example: setMessages([...messages, { sender: "therapist", text: "Response from backend" }]);
    };

    // Function to initialize WebSocket connection
    const initWebSocket = useCallback(() => {
        if (!sessionID) return;

        const ws = new WebSocket(`${websocketURL}/ws/session/${sessionID}`);

        ws.onopen = () => {
            console.log('WebSocket Connected');
            ws.send(JSON.stringify({access_token: user.token}));
        };

        ws.onmessage = (event) => {
            const message = event.data;
            if (message === "Valid token") {
                console.log("Token validated");
                // Handle the incoming messages here
            } else if (message === "Invalid token") {
                console.error("Token is invalid");
                ws.close();
            } else {
                // Handle JSON messages here
                const parsedObjects = JSON.parse(message);
                console.log("Received messages: ", parsedObjects);
                // Append the messages to the chat
                const newMessages = parsedObjects.messages.map((obj) => {
                    return {sender: obj.sender, text: obj.text};
                });
                setMessages([...messages, ...newMessages]);
                console.log("Messages: ", messages);
            }
        };

        ws.onclose = () => {
            console.log('WebSocket Disconnected');
            // Handle disconnection
        };

        ws.onerror = (error) => {
            console.error("WebSocket Error: ", error);
        };

        setWebSocket(ws);

        // Cleanup on component unmount
        return () => {
            ws.close();
        };
    }, [sessionID, user.token, messages]);

    // Effect to initialize WebSocket connection once we have a session ID
    useEffect(() => {
        if (sessionID) {
            initWebSocket();
        }
    }, [sessionID, initWebSocket]);


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
                            <Message key={index} sender={message.sender} text={message.text}/>
                        ))}
                    </Col>
                    <Col style={styles.userChat}>
                        <MessageInput onSendMessage={handleSendMessage}/>
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
