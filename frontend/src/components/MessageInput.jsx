// Code for message input component
import React, { useState } from "react";
import { Form, Button, InputGroup } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-regular-svg-icons';

const MessageInput = ({ onSendMessage }) => {
    const [message, setMessage] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSendMessage(message);
        setMessage("");
    };

    return (
        <Form onSubmit={handleSubmit}>
            <InputGroup className="mb-3">
                <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Type your message..."
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                />
                <Button
                        variant="outline-secondary"
                        type="submit"
                        id="button-addon"
                >
                        <FontAwesomeIcon icon={faPaperPlane} />
                </Button>

            </InputGroup>
        </Form>
    );
};

export default MessageInput;
