/**
 * MovieSphere Dashboard & Playlist Management
 * Logic for Statistics, Watch History, and Playlist CRUD
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Check if user is logged in
    const userData = localStorage.getItem('user_data');
    if (!userData) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Initialize Dashboard
    initDashboard();

    // 3. Initialize specific page logic
    if (document.getElementById('playlists-container')) loadPlaylists();
    if (document.getElementById('favorites-grid')) loadFavorites();
});

async function initDashboard() {
    const user = JSON.parse(localStorage.getItem('user_data'));
    const welcomeText = document.getElementById('welcome-text');
    const userAvatar = document.getElementById('user-avatar');

    if (welcomeText) welcomeText.innerText = `Welcome back, ${user.name}!`;
    
    // Set dynamic avatar to avoid 404 errors
    if (userAvatar) {
        userAvatar.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=E50914&color=fff&bold=true`;
    }

    // Fetch Stats and History in parallel for performance
    try {
        const [historyRes, favsRes] = await Promise.all([
            MovieSphereAPI.request('/user/history'),
            MovieSphereAPI.request('/user/favorites/list')
        ]);

        // Process History
        if (historyRes.ok && historyRes.data) {
            const history = historyRes.data;
            const statWatched = document.getElementById('stat-total-watched');
            if (statWatched) statWatched.innerText = history.length;
            renderHistoryTable(history);
        }

        // Process Favorites & Calculate Stats
        if (favsRes.ok && favsRes.data) {
            const favs = favsRes.data;
            const statFavs = document.getElementById('stat-favorites');
            if (statFavs) statFavs.innerText = favs.length;

            // Calculate Top Genre for Dashboard stats
            if (favs.length > 0) {
                const genres = favs.flatMap(m => m.genres);
                if (genres.length > 0) {
                    const topGenre = genres.sort((a, b) =>
                        genres.filter(v => v === a).length - genres.filter(v => v === b).length
                    ).pop();
                    const statGenre = document.getElementById('stat-top-genre');
                    if (statGenre) statGenre.innerText = topGenre;
                }
            }
        }
    } catch (err) {
        console.error("Dashboard initialization failed:", err);
    }
}

function renderHistoryTable(history) {
    const tableBody = document.getElementById('history-table');
    if (!tableBody) return;

    if (history.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="4" class="p-10 text-center text-gray-500">No watch history yet.</td></tr>`;
        return;
    }

    tableBody.innerHTML = history.slice(0, 5).map(h => {
        // Safe access to nested movie data from history item
        const movie = h.movie || {};
        const watchedDate = h.watched_at ? new Date(h.watched_at).toLocaleDateString() : 'N/A';
        const rating = (movie.rating && typeof movie.rating === 'number') ? movie.rating.toFixed(1) : '0.0';

        return `
            <tr class="border-b border-gray-900 hover:bg-white/5 transition group">
                <td class="p-6">
                    <div class="flex items-center space-x-3">
                        <img src="${movie.poster_path}" class="w-8 h-12 rounded object-cover shadow-lg" onerror="this.src='https://placehold.co/40x60?text=?'">
                        <span class="font-bold text-white">${movie.title || 'Unknown Title'}</span>
                    </div>
                </td>
                <td class="p-6 text-gray-500">${watchedDate}</td>
                <td class="p-6"><span class="text-red-500"><i class="fas fa-star mr-1"></i>${rating}</span></td>
                <td class="p-6">
                    <button onclick="window.location.href='movie-details.html?id=${movie.tmdb_id || movie.id}'" 
                            class="text-xs bg-zinc-800 hover:bg-red-600 px-4 py-1.5 rounded-full transition">
                        View
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

/* Playlist Management */
async function loadPlaylists() {
    const container = document.getElementById('playlists-container');
    if (!container) return;

    container.innerHTML = MovieSphereUI.createSkeleton(); // Show loading state
    
    const { data: playlists, ok } = await MovieSphereAPI.request('/user/playlists');

    if (ok && playlists) {
        if (playlists.length === 0) {
            container.innerHTML = `<div class="col-span-full py-20 text-center text-gray-500">No playlists created yet.</div>`;
            return;
        }

        container.innerHTML = playlists.map(pl => `
            <div class="glass-card rounded-2xl overflow-hidden group hover:border-red-600 transition duration-300">
                <div class="h-40 bg-zinc-900 relative overflow-hidden">
                    <!-- Playlist Preview (Grid of first 4 movies) -->
                    <div class="absolute inset-0 grid grid-cols-2 opacity-30 group-hover:scale-110 transition duration-500">
                        ${pl.movies.slice(0, 4).map(m => `<img src="${m.poster_path}" class="w-full h-full object-cover">`).join('')}
                    </div>
                    <div class="absolute inset-0 flex items-center justify-center">
                        <div class="w-12 h-12 rounded-full bg-red-600 flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300 shadow-xl shadow-red-600/40">
                             <i class="fas fa-play text-white ml-1"></i>
                        </div>
                    </div>
                </div>
                <div class="p-6">
                    <div class="flex justify-between items-start mb-2">
                        <div>
                            <h4 class="font-bold text-xl leading-tight">${pl.name}</h4>
                            <p class="text-gray-500 text-xs mt-1 italic line-clamp-1">${pl.description || 'No description'}</p>
                        </div>
                        <button onclick="deletePlaylist(${pl.id})" class="text-gray-600 hover:text-red-500 p-2 transition">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    <div class="flex justify-between items-center mt-4">
                        <span class="text-xs font-bold text-gray-400 uppercase tracking-widest">${pl.movies.length} Movies</span>
                        <div class="flex -space-x-2">
                            ${pl.movies.slice(0, 3).map(m => `
                                <img src="${m.poster_path}" class="w-7 h-7 rounded-full border-2 border-zinc-900 object-cover shadow-lg" title="${m.title}">
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

async function loadFavorites() {
    const grid = document.getElementById('favorites-grid');
    if (!grid) return;

    grid.innerHTML = Array(6).fill(MovieSphereUI.createSkeleton()).join('');

    const { data: favorites, ok } = await MovieSphereAPI.request('/user/favorites/list');
    if (ok && favorites) {
        if (favorites.length === 0) {
            grid.innerHTML = `<div class="col-span-full py-20 text-center text-gray-500">You haven't favorited any movies yet.</div>`;
            return;
        }
        grid.innerHTML = favorites.map(m => MovieSphereUI.renderMovieCard(m)).join('');
    }
}

function openCreateModal() { 
    document.getElementById('create-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // Stop scrolling behind modal
}

function closeCreateModal() { 
    document.getElementById('create-modal').classList.add('hidden'); 
    document.body.style.overflow = 'auto';
}

async function handleCreatePlaylist() {
    const nameInput = document.getElementById('playlist-name');
    const descInput = document.getElementById('playlist-desc');
    const name = nameInput.value.trim();
    const description = descInput.value.trim();

    if (!name) {
        MovieSphereUI.showToast("Playlist name is required", "error");
        return;
    }

    const { ok } = await MovieSphereAPI.request('/user/playlists', 'POST', { name, description });
    if (ok) {
        MovieSphereUI.showToast("Playlist created successfully!");
        nameInput.value = '';
        descInput.value = '';
        closeCreateModal();
        loadPlaylists();
    }
}

async function deletePlaylist(id) {
    if (!confirm("Are you sure you want to delete this playlist? This cannot be undone.")) return;
    
    const { ok } = await MovieSphereAPI.request(`/user/playlists/${id}`, 'DELETE');
    if (ok) {
        MovieSphereUI.showToast("Playlist deleted");
        loadPlaylists();
    }
}