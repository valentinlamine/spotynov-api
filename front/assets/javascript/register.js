document.addEventListener("DOMContentLoaded", () => {
    const signupBtn = document.querySelector(".signup-btn");
    signupBtn.addEventListener("click", signUp);
});

async function signUp(event) {
    console.log("test"); // Empêcher la soumission du formulaire
    event.preventDefault();

    const userData = {
        username: document.getElementById("pseudo").value,
        password: document.getElementById("password").value
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

    //window.location.replace("http://localhost:8000/login",);
    alert(data.message);
}
