document.addEventListener("DOMContentLoaded", () => {
    const signupBtn = document.querySelector(".signup-btn");
    signupBtn.addEventListener("click", signUp);
});

document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.querySelector("#login-btn");
    loginBtn.addEventListener("click", signIn);
});

async function signUp(event) {
    console.log("test");
    event.preventDefault();

    let passwordField = document.getElementById("confirmPassword");
    let confirmField = document.getElementById("password");

    passwordField.type = "password";
    passwordField.type = "password";

    if (passwordField.value !== confirmField.value) {
        alert("mot de passe mal tapé");
        return;
    }

    const userData = {
        username: document.getElementById("pseudo").value,
        password: passwordField.value
    };

    const response = await fetch("http://127.0.0.1:8000/api/auth/signup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (response.ok) {
        alert("Inscription réussie");
        const response2 = await fetch("http://127.0.0.1:8000/api/auth/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData),
        });

        const data2 = await response2.json();

        if (response2.ok) {
            localStorage.setItem("token", data2.token);
            window.location.href = "http://localhost:8000/home";
        }
    }

    alert(data.message);
}

async function signIn(event) {
    event.preventDefault();

    const pseudo = document.getElementById('pseudo').value;
    const password = document.getElementById('password').value;

    password.type = "password";

    const data = {
        username: pseudo,
        password: password
    };

    try {
        const response = await fetch('http://localhost:8000/api/auth/login', {
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

        localStorage.setItem('token',
            result["token"]);

        window.location.href = 'http://localhost:8000/home';
    } catch (error) {
        alert(error.message);
    }
}


function togglePasswordVisibility(element) {
    const passwordField = element.previousElementSibling; // Trouve l'input avant l'icône
    const isPasswordVisible = passwordField.type === 'password';

    passwordField.type = isPasswordVisible ? 'text' : 'password';
    element.src = isPasswordVisible ? '/assets/icons/Eye.svg' : '/assets/icons/EyeSlash.svg';
}