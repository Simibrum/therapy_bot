// Configuration for the frontend
// ----------------------------------
const backendURL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const websocketURL = backendURL.replace(/^http(s)?:/, 'ws$1:');

export {backendURL, websocketURL};
