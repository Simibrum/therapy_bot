import React, {useCallback, useEffect, useState} from 'react';
import {Col, Container, Row} from 'react-bootstrap';
import SessionCard from './SessionCard';
import NewSessionCard from './NewSessionCard';
import {useUser} from '../UserContext';
import {backendURL} from '../config';

const SessionsList = () => {
    const {user} = useUser();
    const [sessions, setSessions] = useState([]);

    const fetchSessions = useCallback(async () => {
        const apiUrl = `${backendURL}/sessions`;

        const response = await fetch(apiUrl, {
            headers: {
                Authorization: `Bearer ${user.token}`, // Use the token from user context
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch sessions');
        }

        const data = await response.json();
        setSessions(data.sessions);
    }, [user.token]);

    // Function to establish a new therapy session
    const startNewSession = async () => {
        console.log("Starting new session")
        try {
            const response = await fetch(`${backendURL}/sessions/new`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${user.token}`, // Assuming the token is stored in user context
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ /* data if needed */})
            });
            const data = await response.json();
            //setSessionID(data.session_id);
            console.log("New session created with ID: ", data.session_id);
            await fetchSessions();
        } catch (error) {
            console.error("Error starting new session: ", error);
        }
    };

    useEffect(() => {
        if (user.token) {
            fetchSessions();
        }
    }, [user.token, fetchSessions]);

    return (
        <Container>
            <Row xs={1} md={2} lg={3} className="g-4">
                {/* New Session card */}
                <Col>
                    <NewSessionCard onStartNewSession={startNewSession}/>
                </Col>
            </Row>
            <Row xs={1} md={2} lg={3} className="g-4">
                {/* Session cards */}
                {sessions.map((session) => (
                    <Col key={session.id}>
                        <SessionCard session={session}/>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default SessionsList;