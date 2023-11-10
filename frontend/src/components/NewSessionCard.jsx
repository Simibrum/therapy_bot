import React from 'react';
import {Card} from 'react-bootstrap';

const NewSessionCard = ({onStartNewSession}) => {
    return (
        <Card
            bg="success" // This sets the background color to a success green
            text="white"
            style={{width: '18rem', marginBottom: '1rem', cursor: 'pointer'}}
            onClick={onStartNewSession}
        >
            <Card.Body>
                <Card.Title>Start New Session</Card.Title>
            </Card.Body>
        </Card>
    );
};

export default NewSessionCard;
