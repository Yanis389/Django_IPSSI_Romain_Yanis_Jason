const TOTAL_DUELS = 6;
let duelIndex = 0;
let isBusy = false;

function getCookie(name) {
    const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
    return match ? decodeURIComponent(match[1]) : null;
}

function fetchDuelPair() {
    return fetch("/api/duels/pair/").then((r) => r.json());
}

function submitChoice(chosenId, rejectedId) {
    return fetch("/api/duels/choose/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ chosen_id: chosenId, rejected_id: rejectedId }),
    });
}

function renderCard(show, onClick) {
    const card = document.createElement("div");
    card.className = "duel-card";
    card.innerHTML = `
        <img src="${show.poster_url || ''}" alt="${show.title}">
        <h3>${show.title}</h3>
        <p class="genres">${(show.genres || []).join(", ")}</p>
    `;
    card.addEventListener("click", onClick);
    return card;
}

function loadNextDuel() {
    if (duelIndex >= TOTAL_DUELS) {
        document.getElementById("duel-title").hidden = true;
        document.getElementById("duel-pair").hidden = true;
        document.querySelector(".subtitle").hidden = true;
        document.getElementById("duel-skip").hidden = true;
        document.getElementById("duel-done").hidden = false;
        if (typeof loadRecommended === "function") loadRecommended();
        if (typeof loadRadar === "function") loadRadar();
        return;
    }

    document.getElementById("duel-count").textContent = duelIndex + 1;
    document.getElementById("duel-total").textContent = TOTAL_DUELS;

    fetchDuelPair().then(({ show_a, show_b }) => {
        const container = document.getElementById("duel-pair");
        container.innerHTML = "";

        const cardA = renderCard(show_a, () => chooseShow(show_a, show_b));
        const cardB = renderCard(show_b, () => chooseShow(show_b, show_a));

        container.appendChild(cardA);
        container.appendChild(cardB);
        isBusy = false;
    });
}

function chooseShow(chosen, rejected) {
    if (isBusy) return;
    isBusy = true;
    submitChoice(chosen.id, rejected.id).then(() => {
        duelIndex += 1;
        loadNextDuel();
    });
}

function skipDuel() {
    if (isBusy) return;
    isBusy = true;
    loadNextDuel();
}

document.getElementById("duel-skip").addEventListener("click", skipDuel);

loadNextDuel();
