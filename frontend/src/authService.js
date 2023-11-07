// authService.js

export async function handleLogin(username, password) {
  const backendURL = process.env.REACT_APP_BACKEND_URL;
  const apiUrl = backendURL + '/login';
  //const apiUrl = "/login"

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
    console.log(data)
    // Check if token, first_name, and id are available in the response data
    if (data.access_token && data.first_name && data.id) {
      return {
        token: data.access_token,
        firstName: data.first_name,
        id: data.id
      };
    } else {
      throw new Error(`Expected fields are missing in the response data.`);
    }
  } catch (error) {
    throw error;
  }
}
