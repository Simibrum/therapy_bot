// authService.js

export async function handleLogin(username, password) {
  const backendURL = process.env.REACT_APP_BACKEND_URL;
  const apiUrl = backendURL + '/login';

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const message = await response.text();
      throw new Error(`Login failed: ${message}`);
    }

    const data = await response.json();
    return data.token;
  } catch (error) {
    throw error;
  }
}
