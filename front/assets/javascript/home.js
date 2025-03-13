function showMemberInfo(element) {
    const memberId = element.getAttribute("data-id");

    // Simuler des données pour chaque membre
    const membersData = {
        1: { name: "Membre 1", role: "Admin", joined: "Janvier 2024" },
        2: { name: "Membre 2", role: "Modérateur", joined: "Mars 2023" },
        3: { name: "Membre 3", role: "Utilisateur", joined: "Juin 2022" },
        4: { name: "Membre 4", role: "VIP", joined: "Décembre 2021" }
    };

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
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.warn("Aucun token trouvé, redirection vers la page de connexion...");
        window.location.href = "http://localhost:8000/login";  // Redirection vers la page de connexion
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/api/auth/verify-token', {
            method: 'GET',
            headers: { "Authorization": `Bearer ${token}` },
        });

        if (!response.ok) {
            throw new Error(response.detail || "Erreur d'authentification");
        }

        const data = await response.json();
        console.log("Utilisateur authentifié :", data.username);
        // Ici, tu peux mettre à jour l'interface utilisateur avec le username

    } catch (error) {
        console.error("Erreur d'authentification :", error.message);
        localStorage.removeItem("access_token");  // Supprime le token invalide
        window.location.href = "http://localhost:8000/login";  // Redirection vers la connexion
    }
}

// Exécute la vérification dès que la page se charge
document.addEventListener("DOMContentLoaded", checkAuth);

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
