/**
 * MovieSphere Details & Interaction Logic
 * Handles: Metadata fetching, ML Recommendation rendering, User interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const movieId = urlParams.get('id');

    if (!movieId) {
        window.location.href = 'index.html';
        return;
    }

    initializeMovieDetails(movieId);
});

async function initializeMovieDetails(id) {
    const recGrid = document.getElementById('recommendation-grid');
    recGrid.innerHTML = Array(5).fill(MovieSphereUI.createSkeleton()).join('');

    // Fetch Movie Details
    const { data: movie, ok } = await MovieSphereAPI.request(`/movies/${id}`);

    if (ok) {
        renderDetails(movie);
        setupActionButtons(movie.id);
        fetchRecommendations(movie.id);
        
        // Log to watch history (Automatic for logged in users)
        MovieSphereAPI.request('/user/history', 'POST', { movie_id: movie.id });
    } else {
        MovieSphereUI.showToast("Failed to load movie details", "error");
    }
}

function renderDetails(movie) {
    document.title = `${movie.title} | MovieSphere`;
    document.getElementById('movie-backdrop').src = movie.backdrop_path;
    document.getElementById('movie-poster').src = movie.poster_path;
    document.getElementById('movie-title').innerText = movie.title;
    document.getElementById('movie-year').innerText = movie.release_date.split('-')[0];
    document.getElementById('movie-runtime').innerText = `${movie.runtime} min`;
    document.getElementById('movie-lang').innerText = movie.language;
    document.getElementById('movie-overview').innerText = movie.overview;
    document.getElementById('movie-rating').innerText = movie.rating.toFixed(1);
    document.getElementById('movie-director').innerText = movie.director || 'N/A';
    document.getElementById('movie-production').innerText = movie.production || 'N/A';

    // Render Genres
    const genreContainer = document.getElementById('movie-genres');
    genreContainer.innerHTML = movie.genres.map(g => 
        `<span class="bg-zinc-800 text-xs px-3 py-1 rounded-full border border-gray-700">${g}</span>`
    ).join('');

    // Render Cast (Assuming JSON string from backend)
    const castContainer = document.getElementById('movie-cast');
    try {
        const castList = JSON.parse(movie.cast);
        castContainer.innerHTML = castList.slice(0, 5).map(c => 
            `<div class="flex justify-between border-b border-gray-900 pb-1">
                <span class="text-white">${c.name}</span>
                <span class="text-gray-500 text-xs">${c.character}</span>
            </div>`
        ).join('');
    } catch(e) {
        castContainer.innerText = "Cast information unavailable";
    }
}

async function fetchRecommendations(id) {
    const { data: recs, ok } = await MovieSphereAPI.request(`/movies/recommend/${id}`);
    const grid = document.getElementById('recommendation-grid');

    if (ok && recs.length > 0) {
        grid.innerHTML = recs.map(m => MovieSphereUI.renderMovieCard(m)).join('');
    } else {
        grid.innerHTML = `<p class="col-span-full text-center text-gray-500 py-10">No similar movies found.</p>`;
    }
}

function setupActionButtons(movieId) {
    const favBtn = document.getElementById('fav-btn');
    const wlBtn = document.getElementById('watch-later-btn');
    const plBtn = document.getElementById('playlist-btn');

    favBtn.onclick = async () => {
        const { data, ok } = await MovieSphereAPI.request('/user/favorites', 'POST', { movie_id: movieId });
        if (ok) {
            MovieSphereUI.showToast(data.status === 'added' ? "Added to Favorites" : "Removed from Favorites");
            favBtn.querySelector('i').className = data.status === 'added' ? 'fas fa-heart text-red-500 mr-2' : 'far fa-heart mr-2';
        }
    };

    wlBtn.onclick = async () => {
        // Implement Watch Later toggle similar to favorites
        MovieSphereUI.showToast("Added to Watch Later");
    };

    plBtn.onclick = () => openPlaylistModal(movieId);
}

// Modal Logic
function openPlaylistModal(movieId) {
    document.getElementById('playlist-modal').classList.remove('hidden');
    loadUserPlaylists(movieId);
}

function closePlaylistModal() {
    document.getElementById('playlist-modal').classList.add('hidden');
}

async function loadUserPlaylists(movieId) {
    const list = document.getElementById('playlist-list');
    const { data: playlists, ok } = await MovieSphereAPI.request('/user/playlists');

    if (ok && playlists.length > 0) {
        list.innerHTML = playlists.map(pl => `
            <button onclick="addToSpecificPlaylist(${pl.id}, ${movieId})" class="w-full flex items-center justify-between p-4 bg-zinc-900 rounded-xl hover:bg-zinc-800 transition">
                <span class="font-bold">${pl.name}</span>
                <span class="text-xs text-gray-500">${pl.movies.length} movies</span>
            </button>
        `).join('');
    } else {
        list.innerHTML = `<p class="text-center text-gray-500 text-sm py-4">No playlists found.</p>`;
    }
}

async function addToSpecificPlaylist(playlistId, movieId) {
    const { ok } = await MovieSphereAPI.request(`/user/playlists/${playlistId}/add`, 'POST', { movie_id: movieId });
    if (ok) {
        MovieSphereUI.showToast("Added to Playlist!");
        closePlaylistModal();
    }
}