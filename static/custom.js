async function editinfo(username) {
    const token = document.cookie.split("access_token=")[1]?.split(";")[0]; // Extract the token from cookies

    try {
        const response = await fetch('/post_edit_users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, token: token })
        });

        const result = await response.json(); // Parse JSON response

        if (response.ok) {
            window.location.href = `${result.redirect_url}?username=${result.username}`;
        } else {
            console.error('Unexpected response:', result);
            alert('An error occurred. Please try again.');
        }
    } catch (error) {
        console.error('Network Error:', error);
        alert('Network error. Please check your connection and try again.');
    }
}

