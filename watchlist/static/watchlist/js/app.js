function getCookie(name) {
    const cookie = document.cookie
        .split('; ')
        .find(c => c.startsWith(name + '='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
}

function apiPost(url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data || {}),
    });
}

function apiDelete(url) {
    return fetch(url, {
        method: 'DELETE',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
    });
}

function carteSerie(show) {
    const note = show.vote_average ? show.vote_average.toFixed(1) : '-';
    const image = show.poster_url
        ? `<img src="${show.poster_url}" alt="${show.title}">`
        : '<div class="poster-vide">Pas d\'affiche</div>';
    return `
        <a class="carte" href="/shows/${show.id}/">
            ${image}
            <div class="carte-titre">${show.title}</div>
            <div class="carte-note">${note}</div>
        </a>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const lienLogout = document.getElementById('nav-logout');
    if (lienLogout) {
        lienLogout.addEventListener('click', (e) => {
            e.preventDefault();
            apiPost('/api/auth/logout/').then(() => {
                window.location.href = '/';
            });
        });
    }
});
