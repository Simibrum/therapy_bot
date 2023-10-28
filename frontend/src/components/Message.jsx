// Code for the message component
import React from 'react';

const Message = ({ sender, text }) => {
    if (sender === "therapist") {
        return <div style={styles.therapistMessage}>{text}</div>;
    } else {
        return <div style={styles.userMessage}>{text}</div>;
    }
};

const styles = {
    therapistMessage: {
        backgroundColor: "#e0e0e0",
        borderRadius: "15px",
        padding: "10px",
        margin: "5px 0",
        alignSelf: "flex-start"
    },
    userMessage: {
        backgroundColor: "#4CAF50",
        color: "white",
        borderRadius: "15px",
        padding: "10px",
        margin: "5px 0",
        alignSelf: "flex-end"
    }
};

export default Message;