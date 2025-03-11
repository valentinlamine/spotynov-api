document.addEventListener("DOMContentLoaded", () => {
    const signupBtn = document.querySelector(".signup-btn");
    if (signupBtn) signupBtn.addEventListener("click", signUp);

    const loginBtn = document.querySelector(".login-btn");
    if (loginBtn) loginBtn.addEventListener("click", signIn);

    checkAuthOnHome();
});

async function signUp(event) {
    event.preventDefault();

    let passwordField = document.getElementById("password");
    let confirmField = document.getElementById("confirmPassword");

    if (passwordField.value !== confirmField.value) {
        alert("Mot de passe mal tapé");
        return;
    }

    const userData = {
        username: document.getElementById("pseudo").value,
        password: passwordField.value
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/api/auth/signup/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData),
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail || "Erreur lors de l'inscription");

        alert("Inscription réussie, connexion en cours...");

        // Connexion automatique après l'inscription
        await signIn(event, userData);
    } catch (error) {
        alert(error.message);
    }
}

async function signIn(event, userData = null) {
    if (event) event.preventDefault();

    const pseudo = userData ? userData.username : document.getElementById("pseudo").value;
    const password = userData ? userData.password : document.getElementById("password").value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: pseudo, password: password }),
        });

        const result = await response.json();

        if (!response.ok) throw new Error(result.detail || "Identifiants incorrects");

        localStorage.setItem("token", result.token);
        window.location.href = "home"; // Redirection après connexion
    } catch (error) {
        alert(error.message);
    }
}

// 🔐 Vérifie si l'utilisateur est connecté avant d'afficher la page home
async function checkAuthOnHome() {
    if (!window.location.pathname.includes("home")) return;

    const token = localStorage.getItem("token");

    if (!token) {
        alert("Vous devez être connecté pour accéder à cette page.");
        window.location.href = "http://127.0.0.1:8000/login"; // Redirection vers la connexion
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/auth/verify-token", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error("Session expirée ou accès non autorisé");

        const data = await response.json();
        document.getElementById("welcome-message").innerText = data.message;
    } catch (error) {
        alert(error.message);
        localStorage.removeItem("token"); // Supprime le token en cas d'erreur
        window.location.href = "http://127.0.0.1:8000/login"; // Redirection vers la connexion
    }
}


function togglePasswordVisibility(element) {
    const passwordField = document.getElementById('password');
    const isPasswordVisible = passwordField.type === 'password';

    passwordField.type = isPasswordVisible ? 'text' : 'password';
    element.src = isPasswordVisible ? '/assets/icons/Eye.svg' : '/assets/icons/EyeSlash.svg';
}

function toggleConfirmPasswordVisibility(element) {
    const passwordField = document.getElementById('confirmPassword');
    const isConfirmPasswordVisible = passwordField.type === 'password';

    passwordField.type = isConfirmPasswordVisible ? 'text' : 'password';
    element.src = isConfirmPasswordVisible ? '/assets/icons/Eye.svg' : '/assets/icons/EyeSlash.svg';
}