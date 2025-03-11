document.addEventListener("DOMContentLoaded", () => {
    const signupBtn = document.querySelector(".signup-btn");
    if (signupBtn) signupBtn.addEventListener("click", signUp);

    const loginBtn = document.querySelector(".login-btn");
    if (loginBtn) loginBtn.addEventListener("click", signIn);
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
        const response = await fetch("http://localhost:8000/api/auth/signup/", {
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
    console.log(JSON.stringify({ username: pseudo, password: password }))
    try {
        const response = await fetch('http://localhost:8000/api/auth/login/', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: pseudo, password: password }),
        });

        const result = await response.json();

        if (!response.ok) throw new Error(result.detail || "Identifiants incorrects");

        localStorage.setItem("token", result.token);

        const response2 = await fetch("http://localhost:8000/home", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${result.token}`
            }
        })

        window.location.href = "home";
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