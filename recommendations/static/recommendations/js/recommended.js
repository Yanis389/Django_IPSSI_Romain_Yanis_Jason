function renderRecommendedCard(show) {
    const card = document.createElement("a");
    card.className = "recommended-card";
    card.href = `/shows/${show.id}/`;
    card.innerHTML = `
        <img src="${show.poster_url || ''}" alt="${show.title}">
        <h3>${show.title}</h3>
    `;
    return card;
}

function loadRecommended() {
    const section = document.getElementById("recommended-section");
    const container = document.getElementById("recommended-grid");
    if (!section || !container) return;

    fetch("/api/recommendations/")
        .then((r) => (r.ok ? r.json() : []))
        .then((shows) => {
            if (!shows.length) return;
            container.innerHTML = "";
            shows.forEach((show) => container.appendChild(renderRecommendedCard(show)));
            section.hidden = false;
        })
        .catch(() => {});
}

loadRecommended();
