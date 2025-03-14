document.addEventListener("DOMContentLoaded", () => {
    const signupBtn = document.querySelector(".signup-btn");
    if (signupBtn) signupBtn.addEventListener("click", signUp);

    const loginBtn = document.querySelector(".login-btn");
    if (loginBtn) loginBtn.addEventListener("click", signIn);
});

const PORT=8000;
const FIRST_URI="http://localhost:"+PORT;

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
        const response = await fetch(FIRST_URI + "/api/auth/signup/", {
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

    const pseudo = document.getElementById("pseudo").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(FIRST_URI + '/api/auth/login/', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: pseudo, password: password }),
        });

        const result = await response.json();

        // Vérifier si la connexion a réussi
        if (response.ok && result.detail === "Connexion réussie") {
            // Stocker le token d'accès dans localStorage (ou sessionStorage si vous préférez)
            localStorage.setItem("access_token", result.access_token);

            const response2 = await fetch(FIRST_URI + '/api/auth/verify-token', {
                method: 'GET',
                headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
            });

            // Rediriger vers la page /home après la connexion
            window.location.href = "/home";
        } else {
            // Afficher un message d'erreur si la connexion échoue
            alert(result.detail || "Erreur de connexion");
        }
    } catch (error) {
        alert(error.message || "Erreur de connexion. Veuillez réessayer.");
    }
}


function togglePasswordVisibility(element) {
    const passwordField = element.previousElementSibling; // Trouve l'input avant l'icône
    const isPasswordVisible = passwordField.type === 'password';

    passwordField.type = isPasswordVisible ? 'text' : 'password';
    element.src = isPasswordVisible ? '/assets/icons/Eye.svg' : '/assets/icons/EyeSlash.svg';
}