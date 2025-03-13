// Exécute la vérification dès que la page se charge
document.addEventListener("DOMContentLoaded", checkAuth);

// Charger les groupes au chargement de la page
document.addEventListener("DOMContentLoaded", loadGroups);

document.addEventListener("DOMContentLoaded", () => {
    const refreshBtn = document.querySelector(".refresbutton");
    if (refreshBtn) refreshBtn.addEventListener("click", spotifyConnect);
});

async function spotifyConnect() {
    if (event) event.preventDefault();

    const response = await fetch("http://localhost:8000/api/spotify/connect/", {
        method: "GET",
        headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
    });

    const result = await response.json();

    let access;
    if (response.ok) {
        access = window.location.href = result.auth_url;
    } else console.log("erreur")

    console.log(access);



}

async function loadGroups() {
    try {
        const response = await fetch("http://localhost:8000/api/group/list", {
            method: "GET",
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des groupes");
        }

        const groups = await response.json().groups;
        console.log("Groupes reçus :", groups);

        const currentGroupContainer = document.querySelector(".column-side-top-section .track");
        const otherGroupsContainer = document.querySelector(".column-side-bottom-section");

        currentGroupContainer.innerHTML = "";
        otherGroupsContainer.innerHTML = "<h2>Autres Groupes</h2>";

        let currentGroupFound = false;

        groups.forEach(group => {
            // Vérifier si l'utilisateur connecté est membre de ce groupe
            const isCurrentUserInGroup = group.members.includes(parseInt(userId));

            const groupElement = document.createElement("div");
            groupElement.classList.add("track");
            groupElement.innerHTML = `
                <img src="../assets/icons/Chats.svg" alt="Cover" class="track-img">
                <a href="group.html?id=${group.name}" class="track-name">${group.name}</a>
            `;

            if (isCurrentUserInGroup && !currentGroupFound) {
                // Si l'utilisateur est membre du groupe, et que c'est le premier trouvé
                currentGroupContainer.appendChild(groupElement);
                currentGroupFound = true;
            } else {
                // Sinon, c'est un "autre groupe"
                otherGroupsContainer.appendChild(groupElement);
            }
        });

        // Si aucun groupe principal n'a été trouvé, afficher un message
        if (!currentGroupFound) {
            currentGroupContainer.innerHTML = "<span>Aucun groupe principal</span>";
        }

    } catch (error) {
        console.error("Erreur :", error.message);
    }
}

async function showMemberInfo(element) {
    const memberId = element.getAttribute("data-id");

    const response = await fetch('http://localhost:8000/api/groups/members', {
        method: 'GET',
        headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
    });

    const result = await response.json();

    // Simuler des données pour chaque membre
    /*const membersData = {
        1: { name: "Membre 1", role: "Admin", joined: "Janvier 2024" },
        2: { name: "Membre 2", role: "Modérateur", joined: "Mars 2023" },
        3: { name: "Membre 3", role: "Utilisateur", joined: "Juin 2022" },
        4: { name: "Membre 4", role: "VIP", joined: "Décembre 2021" }
    };*/

    let membersData;
    membersData = result;
    console.log(membersData)

    // Récupérer les infos du membre sélectionné
    const memberInfo = membersData[memberId];

    // Sélectionner la colonne et remplacer son contenu
    const column = document.querySelector(".right-column-side");
    column.innerHTML = `
        <div class="right-column-side-top-section">
            <h2>Profil de ${memberInfo.name}</h2>
        </div>
        <div class="right-column-side-bottom-section">
            <p><strong>Rôle :</strong> ${memberInfo.role}</p>
            <p><strong>Date d'adhésion :</strong> ${memberInfo.joined}</p>
            <button class="back-btn" onclick="reloadMemberList()">Retour</button>
        </div>
    `;
}

function reloadMemberList() {
    document.querySelector(".right-column-side").innerHTML = `
        <div class="right-column-side-top-section">
            <h2>Membre(s) du groupe</h2>
        </div>
        <div class="right-column-side-bottom-section" id="membersList">
            <div class="memberlist" data-id="1" onclick="showMemberInfo(this)">
                <span class="member-name">Membre 1</span>
            </div>
            <div class="memberlist" data-id="2" onclick="showMemberInfo(this)">
                <span class="member-name">Membre 2</span>
            </div>
            <div class="memberlist" data-id="3" onclick="showMemberInfo(this)">
                <span class="member-name">Membre 3</span>
            </div>
            <div class="memberlist" data-id="4" onclick="showMemberInfo(this)">
                <span class="member-name">Membre 4</span>
            </div>
        </div>
    `;
}


async function checkAuth() {
    const body = document.querySelector(".homeBody");
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.warn("Aucun token trouvé, redirection vers la page de connexion...");
        body.style.display = "none";
        window.location.href = "http://localhost:8000/login";  // Redirection vers la page de connexion
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/api/auth/verify-token', {
            method: 'GET',
            headers: { "Authorization": `Bearer ${token}` },
        });

        if (!response.ok) {
            body.style.display = "none";
            throw new Error(response.detail || "Erreur d'authentification");
        } else {

            const data = await response.json();
            console.log("Utilisateur authentifié :", data.username);
            body.style.display = "flex";
        }
    } catch (error) {
        console.error("Erreur d'authentification :", error.message);
        localStorage.removeItem("access_token");  // Supprime le token invalide
        window.location.href = "http://localhost:8000/login";  // Redirection vers la connexion
    }
}

function showColumn(columnId) {
    // Cache toutes les colonnes
    document.querySelectorAll('.column').forEach(column => {
        column.style.display = 'none';
    });

    // Affiche la colonne spécifiée
    document.getElementById(columnId).style.display = 'block';

    // Ajoute la classe "active" au bouton sélectionné
    document.querySelectorAll('.mobile-nav button').forEach(button => {
        button.classList.remove('active');
    });
    document.querySelector(`.mobile-nav button[onclick="showColumn('${columnId}')"]`).classList.add('active');
}

function logout() {
    // Redirige ou effectue une action de déconnexion
    console.log('Déconnexion');
}

// Fonction qui s'active lors du redimensionnement de l'écran
window.addEventListener('resize', function() {
    if (window.innerWidth > 1080) {
        // Réaffiche toutes les colonnes en mode desktop
        document.querySelectorAll('.column').forEach(column => {
            column.style.display = 'block';
        });
        // Cache la navigation mobile
        document.querySelector('.mobile-nav').style.display = 'none';
    } else {
        // Affiche la navigation mobile en mode mobile
        document.querySelector('.mobile-nav').style.display = 'flex';

        // Sélectionne la colonne de musique par défaut lorsqu'on passe en mode mobile
        showColumn('column-middle');
    }
});

// Vérification initiale au chargement de la page
if (window.innerWidth > 1080) {
    document.querySelectorAll('.column').forEach(column => {
        column.style.display = 'block'; // Affiche toutes les colonnes en mode desktop
    });
    document.querySelector('.mobile-nav').style.display = 'none'; // Cache la barre de navigation mobile en desktop
} else {
    document.querySelector('.mobile-nav').style.display = 'flex'; // Affiche la navigation mobile en mode mobile
    // Sélectionne la colonne de musique par défaut en mode mobile
    showColumn('column-middle');
}


