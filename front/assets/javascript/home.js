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
