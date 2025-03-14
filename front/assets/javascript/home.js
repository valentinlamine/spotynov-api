document.addEventListener("DOMContentLoaded", () => {
    checkAuth();  // Vérifie l'authentification
    loadGroups(); // Charge les groupes
    loadTracks(""); // Charge les tracks
    loadMembers();

    // Ajoute un event listener au bouton "refresh" si présent
    const refreshBtn = document.querySelector(".refreshbutton");
    if (refreshBtn) refreshBtn.addEventListener("click", spotifyConnect);
});

const PORT=8000;
const FIRST_URI="http://localhost:"+PORT;

async function spotifyConnect() {
    if (event) event.preventDefault();

    const response = await fetch(FIRST_URI + "/api/spotify/connect/", {
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
        const response = await fetch(FIRST_URI + "/api/groups/list", {
            method: "GET",
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
        });

        const response2 = await fetch(FIRST_URI + "/api/groups/get-group", {
            method: "POST",
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des groupes");
        }
        if (!response2.ok) {
            console.log("no main group found");
        }

        const result = await response.json();
        const result2 = await response2.json();
        let groups = result.groups;
        let mainGroupName = result2.group;

        console.log("Groupes reçus :", groups, "main group: ", mainGroupName);

        const mainGroup = document.querySelector(".main-group");
        const otherGroup = document.querySelector(".other-groups");

        mainGroup.innerHTML += `<div class="track ">
                        <img src="../assets/icons/Chats.svg" alt="Cover" class="track-img">
                        <span class="track-name">${mainGroupName}</span>
                        <img src="../assets/icons/Deconnexion.svg" alt="Cover" class="track-img" id="leaveGroupBtn" onclick="leaveGroup()">

                        </div>`

        groups.forEach(group => {
            otherGroup.innerHTML += `<div class="track">
                        <img src="../assets/icons/Chats.svg" alt="Cover" class="track-img">
                        <span class="track-name" onclick="joinGroup(this)">${group}</span>
                        </div>`;
        });

        // Si aucun groupe principal n'a été trouvé, afficher un message
        if (!mainGroupName) {
            mainGroup.innerHTML = "<span class='track-name'>Vous n'avez pas de groupe</span> ";
        }

    } catch (error) {
        console.error("Erreur :", error.message);
    }
}

async function joinGroup(e) {
    const groupName = e.innerHTML; // Récupère le nom du groupe à partir du DOM

    if (!groupName) {
        throw new Error("Le nom du groupe est vide ou invalide");
    }

    console.log("Tentative de rejoindre le groupe : ", groupName);

    try {
        // Envoie la requête pour rejoindre un groupe
        const response = await fetch(FIRST_URI + "/api/groups/join", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: groupName }), // Envoie le nom du groupe dans le corps de la requête
        });

        const result = await response.json();

        if (!response.ok) {
            // Si la réponse indique que l'utilisateur est déjà dans ce groupe, on gère cela proprement
            if (result.detail && result.detail === "Vous êtes déjà dans ce groupe") {
                alert("Vous êtes déjà membre de ce groupe !");
            } else {
                throw new Error(result.detail || "Erreur lors de l'adhésion au groupe");
            }
        } else {
            console.log("Groupe rejoint avec succès : ", result);
            alert("Vous avez rejoint le groupe avec succès !");
            window.location.reload(); // Recharge la page si nécessaire pour mettre à jour l'UI
        }

    } catch (error) {
        console.error("Erreur : ", error.message);
        alert("Une erreur est survenue, veuillez réessayer.");
    }
}

async function showMemberInfo(element) {
    try {
        const memberName = element.textContent.trim();

        /*const response = await fetch('http://localhost:8001/api/groups/member-info', {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ member: memberName })
        });



        const memberInfo = await response.json();
        if (!response.ok) {
            throw new Error(memberInfo.detail || "Erreur lors de la récupération des informations du membre");
        }
         */
        const column = document.querySelector(".right-column-side");
        column.innerHTML = `
            <div class="right-column-side-top-section">
                <h2>Profil de ${memberName}</h2>
            </div>
            <div class="right-column-side-bottom-section" style="overflow: hidden;">
                <p><strong>Personnalité :</strong> role</p>
                <p><strong>Personnalité 2 :</strong> role2</p>
                <button class="back-btn" onclick="reloadMemberList()">Retour</button>
                <button class="back-btn" onclick="${await stealTracks(memberName)}">Voler les titres likés</button>
            </div>
        `;
    } catch (error) {
        console.error("Erreur lors de la récupération des informations du membre :", error);
    }
}

async function reloadMemberList() {
    try {
        await loadMembers();
    } catch (error) {
        console.error("Erreur lors du rechargement des membres :", error);
    }
}


async function checkAuth() {
    const body = document.querySelector(".homeBody");
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.warn("Aucun token trouvé, redirection vers la page de connexion...");
        body.style.display = "none";
        window.location.href = FIRST_URI + "/login";  // Redirection vers la page de connexion
        return;
    }

    try {
        const response = await fetch(FIRST_URI + '/api/auth/verify-token', {
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
        window.location.href = FIRST_URI + "/login";  // Redirection vers la connexion
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
    localStorage.removeItem("access_token");

    window.location.href = FIRST_URI + "/login";
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


document.addEventListener("DOMContentLoaded", () => {
    const groupNameInput = document.querySelector("#groupName");

    // Écouter l'événement "keypress" sur le champ de saisie pour valider avec "Enter"
    if (groupNameInput) {
        groupNameInput.addEventListener("keypress", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();  // Empêcher le comportement par défaut du "Enter" (par exemple, envoyer un formulaire)
                createGroup();  // Créer le groupe lorsque l'Utilisateur appuie sur "Enter"
            }
        });
    }
});

async function createGroup() {
    const groupName = document.getElementById("groupName").value;
    const accessToken = localStorage.getItem("access_token");

    // Vérification de l'existence du token d'accès
    if (!accessToken) {
        alert("Vous devez être connecté pour créer un groupe");
        return;
    }

    if (!groupName) {
        alert("Le nom du groupe ne peut pas être vide");
        return;
    }

    try {
        const response = await fetch(FIRST_URI + "/api/groups/create", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: groupName }),
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la création du groupe");
        }

        const result = await response.json();
        console.log("Groupe créé :", result.group);

        // Afficher un message ou rediriger l'utilisateur après la création
        alert("Le groupe a été créé avec succès !");
        window.location.reload(); // Recharger la page ou rediriger l'utilisateur vers une autre page si nécessaire
    } catch (error) {
        console.error("Erreur :", error.message);
        alert("Une erreur est survenue. Veuillez réessayer.");
    }
}

// Fonction pour quitter le groupe
async function leaveGroup() {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        alert("Vous devez être connecté pour quitter un groupe");
        return;
    }

    try {
        const response = await fetch(FIRST_URI + "/api/groups/leave", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({}),
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la sortie du groupe");
        }

        const result = await response.json();
        console.log("Groupe quitté avec succès", result);

        // Optionnel : Met à jour l'interface pour refléter que l'utilisateur a quitté le groupe
        alert("Vous avez quitté le groupe avec succès!");

        // Redirection ou actualisation de l'interface
        window.location.reload(); // Ou rediriger vers une autre page si nécessaire

    } catch (error) {
        console.error("Erreur :", error.message);
        alert("Une erreur est survenue. Veuillez réessayer.");
    }
}

async function loadTracks(name) {
    console.log("name", name);
    const trackList = document.querySelector(".playlist");

    // Vérifie si le token d'accès est présent dans le localStorage
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
        alert("Vous devez être connecté pour voir vos morceaux.");
        return;
    }

    try {
        // Modifie la méthode en POST, et place les paramètres dans le corps
        const username = name;  // Remplace par le nom d'utilisateur réel
        const limit = 10;  // Nombre de morceaux à récupérer
        const response = await fetch(FIRST_URI + "/api/spotify/last-liked-songs", {
            method: "POST",  // Changement de méthode pour POST
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({  // Ajoute les paramètres dans le corps de la requête
                username: username,
                limit: limit
            })
        });

        // Vérifie si la réponse est correcte
        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des morceaux");
        }

        const result = await response.json();
        const likedSongs = result.liked_songs;

        // Vérifie si des morceaux sont disponibles
        if (!likedSongs || likedSongs.length === 0) {
            trackList.innerHTML = "<p>Aucun morceau aimé trouvé.</p>";
            return;
        }

        trackList.innerHTML = `<div class="track-info header-track">
                            <span class="track-number">#</span>
                            <span class="track-img-placeholder"></span> <!-- Espace vide pour aligner -->
                            <span class="track-name">Titre</span>
                            <img src="../assets/icons/Timer.svg" alt="Options" class="track-options-icon">
                        </div>
                        <span class="separator"></span>`
        // Parcours les morceaux et les ajoute dynamiquement à la playlist
        likedSongs.forEach((song, index) => {
            // Ajoute chaque chanson à la playlist
            trackList.innerHTML += `
                <div class="track">
                    <span class="track-number">${index + 1}</span>
                    <img src="${song["track"]["album"]["images"][0]["url"] || "../assets/background/rectangle-1.png"}" alt="Cover" class="track-img">
                    <span class="track-name">${song["track"].name || "Nom de la musique"}</span>
                    <span class="track-time">${formatDuration(song["track"].duration_ms || "0:00")}</span>
                </div>
            `;
        });

    } catch (error) {
        console.error("Erreur : ", error.message);
    }
}

// Fonction pour formater la durée d'une chanson (en secondes) en format mm:ss
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60000);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}


async function loadMembers() {
    try {
        // Récupérer l'admin du groupe
        const adminResponse = await fetch(FIRST_URI + "/api/groups/get-admin", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json"
            },
        });

        const adminResult = await adminResponse.json();
        if (!adminResponse.ok) {
            throw new Error(adminResult.detail || "Erreur lors de la récupération de l'admin");
        }

        // Récupérer la liste des membres
        const membersResponse = await fetch(FIRST_URI + "/api/groups/members", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
        });

        const membersResult = await membersResponse.json();
        if (!membersResponse.ok) {
            throw new Error(membersResult.detail || "Erreur lors de la récupération des membres");
        }

        const membersList = document.querySelector(".right-column-side");

        // Vérifie si la liste des membres existe
        if (membersResult.members && membersResult.members.length > 0) {
            membersList.innerHTML = `
                <div class="right-column-side-top-section">
                    <h2>Admin du groupe</h2>
                </div>
                <div class="right-column-side-bottom-section" id="adminSection">
                    <!-- Admin sera inséré ici -->
                </div>
                <div class="right-column-side-top-section">
                    <h2>Membre(s) du groupe</h2>
                </div>
                <div class="right-column-side-bottom-section" id="membersList">
                    <!-- Membres seront insérés ici -->
                </div>
            `;

            // Insertion de l'admin dans la section "Admin du groupe"
            const adminSection = document.querySelector("#adminSection");
            const adminDiv = document.createElement("div");
            adminDiv.classList.add("memberlist");
            adminDiv.innerHTML = `<span class="member-name" onclick="loadTracks(this.innerHTML)">${adminResult.admin}</span>`;
            adminSection.appendChild(adminDiv);
            adminSection.onclick = function () {
                showMemberInfo(this);
            };

            // Création des éléments pour chaque membre (hors admin)
            const membersSection = document.querySelector("#membersList");
            for (const member of membersResult.members) {
                const index = membersResult.members.indexOf(member);
                if (member !== adminResult.admin) { // Exclure l'admin de la liste des membres
                    const memberDiv = document.createElement("div");
                    memberDiv.classList.add("memberlist");
                    memberDiv.setAttribute("data-id", member);
                    memberDiv.innerHTML = `<span class="member-name" onclick="loadTracks(this.innerHTML)">${member}</span>`;
                    memberDiv.onclick = function () {
                        showMemberInfo(this);
                    };
                    membersSection.appendChild(memberDiv);
                }
            }
        } else {
            membersList.innerHTML = "<p>Aucun membre trouvé.</p>";
        }
    } catch (error) {
        console.error("Erreur lors du chargement des membres :", error);
        document.querySelector(".right-column-side").innerHTML = "<p>Une erreur est survenue. Veuillez réessayer plus tard.</p>";
    }
}

async function stealTracks(name) {
    console.log(name);
    try {
        const response = await fetch(FIRST_URI + "/api/spotify/create-playlist-from-likes", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user: name,
            })
        });

        const result = await response.json();
    }catch (error){
        alert("Erreur lors du vol de la playlist");
    }
}

async function synchronize(){
    try {
        const response = await fetch(FIRST_URI + '/api/spotify/synchronize', {
            method: 'POST',
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` },
        });

        const result = await response.json();
    }
    catch (error) {
        alert("Vérifiez que vous êtes admin ou pas seul dans le groupe");
    }
}