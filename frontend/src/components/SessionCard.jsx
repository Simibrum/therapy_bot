import React from 'react';
import {Card} from 'react-bootstrap';
import {useNavigate} from "react-router-dom";

const SessionCard = ({session}) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/sessions/${session.id}`);
  };

  return (
      <Card style={{width: '18rem', marginBottom: '1rem', cursor: 'pointer'}} onClick={handleCardClick}>
        <Card.Body>
          <Card.Title>Session {session.id}</Card.Title>
          <Card.Text>
            Therapist ID: {session.therapist_id}
            <br/>
            Start Time: {session.start_time}
            <br/>
            End Time: {session.end_time || 'Ongoing'}
          </Card.Text>
        </Card.Body>
      </Card>
  );
};

export default SessionCard;
