document.addEventListener("DOMContentLoaded", () => {
    document.querySelector(".signup-btn").addEventListener("click", signUp);
});

async function signUp() {
    const userData = {
        username: document.getElementById("pseudo").value,
        password: document.getElementById("password").value
    };
    console.log(JSON.stringify(userData));

    const response = await fetch("http://127.0.0.1:8000/api/auth/signup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData),
    });

    const data = await response.json();
    alert(data.message);
}