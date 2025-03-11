async function signIn(event) {
    event.preventDefault();

    const pseudo = document.getElementById('pseudo').value;
    const password = document.getElementById('password').value;

    const data = {
        username: pseudo,
        password: password
    };

    try {
        const response = await fetch('http://localhost:8000/api/auth/login', { // Assurez-vous que l'URL correspond
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Identifiants incorrects');
        }

        const result = await response.json();

        localStorage.setItem('token', result.token);

        window.location.href = '/dashboard';
    } catch (error) {
        alert(error.message);
    }
}


function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
}