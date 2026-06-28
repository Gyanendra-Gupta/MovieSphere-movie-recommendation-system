/**
 * MovieSphere Core Application Logic
 * Role: API Wrapper, State Manager, UI Utilities
 */

const API_BASE_URL = "http://localhost:5000/api";

class MovieSphereAPI {
    static async request(endpoint, method = 'GET', body = null) {
        const token = localStorage.getItem('access_token');
        const headers = { 'Content-Type': 'application/json' };

        // STRICT CHECK: Only add header if token is a valid JWT string
        // This prevents the 422 Unprocessable Entity error
        if (token && token !== "null" && token !== "undefined" && token.length > 20) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers,
            ...(body && { body: JSON.stringify(body) })
        };

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            
            if (response.status === 401) {
                MovieSphereUI.handleUnauthorized();
                return { data: null, ok: false, status: 401 };
            }

            if (response.status === 204) return { data: null, ok: true };

            const data = await response.json();
            return { data, status: response.status, ok: response.ok };
        } catch (error) {
            console.error("MovieSphere API Error:", error);
            return { data: null, ok: false };
        }
    }
}

class MovieSphereUI {
    static showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-600' : 'bg-red-600';
        
        toast.className = `${bgColor} text-white px-6 py-3 rounded-lg shadow-xl toast-in mb-3 flex items-center justify-between min-w-[300px]`;
        toast.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" class="ml-4 font-bold focus:outline-none">&times;</button>
        `;
        
        container.appendChild(toast);
        setTimeout(() => { if(toast.parentElement) toast.remove(); }, 4000);
    }

    static handleUnauthorized() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
        const publicPages = ['/login.html', '/register.html', '/index.html'];
        if (!publicPages.includes(window.location.pathname)) {
            window.location.href = 'login.html';
        }
    }

    static createSkeleton() {
        return `<div class="movie-card relative rounded-lg overflow-hidden h-72 skeleton bg-zinc-800 animate-pulse"></div>`;
    }

    static renderMovieCard(movie) {
        const movieId = movie.id || movie.tmdb_id;
        const title = movie.title || 'Untitled Movie';
        
        // FIX: Using placehold.co (more reliable) + custom styling
        const fallbackPoster = `https://placehold.co/500x750/1a1a1a/ffffff?text=${encodeURIComponent(title)}`;
        
        // Use poster_path if it's a valid URL, else use fallback
        const poster = (movie.poster_path && movie.poster_path.startsWith('http')) 
                       ? movie.poster_path 
                       : fallbackPoster;

        const rating = (movie.rating && typeof movie.rating === 'number') ? movie.rating.toFixed(1) : '0.0';
        const year = (movie.release_date && typeof movie.release_date === 'string') ? movie.release_date.split('-')[0] : 'N/A';

        return `
            <div class="movie-card relative rounded-lg overflow-hidden h-72 cursor-pointer shadow-lg group bg-zinc-900" 
                 onclick="window.location.href='movie-details.html?id=${movieId}'">
                <img src="${poster}" alt="${title}" class="w-full h-full object-cover transition duration-300 group-hover:scale-110" 
                     onerror="this.onerror=null;this.src='${fallbackPoster}';">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
                    <h4 class="font-bold text-sm line-clamp-2">${title}</h4>
                    <div class="flex items-center text-xs text-red-500 mt-1">
                        <span class="mr-2"><i class="fas fa-star mr-1"></i>${rating}</span>
                        <span class="text-gray-300">${year}</span>
                    </div>
                </div>
            </div>
        `;
    }
}

// Global Auth UI Update
document.addEventListener('DOMContentLoaded', () => {
    const userData = localStorage.getItem('user_data');
    if (!userData) return;

    try {
        const user = JSON.parse(userData);
        const authNav = document.getElementById('auth-nav');
        
        if (user && authNav) {
            // FIX: Using UI-Avatars for a professional fallback instead of missing local image
            const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=E50914&color=fff&bold=true`;
            
            authNav.innerHTML = `
                <div class="relative group">
                    <button class="flex items-center space-x-3 focus:outline-none py-1">
                        <img src="${avatarUrl}" 
                             class="w-8 h-8 rounded-md border border-gray-700 object-cover"
                             alt="Profile">
                        <span class="hidden md:block text-sm font-medium hover:text-red-500 transition">${user.name}</span>
                        <i class="fas fa-chevron-down text-[10px] text-gray-500 group-hover:text-red-500 transition"></i>
                    </button>
                    <div class="absolute right-0 w-48 mt-2 bg-[#141414] border border-gray-800 rounded-md shadow-2xl hidden group-hover:block z-50 overflow-hidden">
                        <a href="dashboard.html" class="block px-4 py-3 text-sm hover:bg-zinc-800 transition">
                            <i class="fas fa-th-large mr-2 text-gray-500"></i> Dashboard
                        </a>
                        <a href="profile.html" class="block px-4 py-3 text-sm hover:bg-zinc-800 transition">
                            <i class="fas fa-user-edit mr-2 text-gray-500"></i> Profile
                        </a>
                        <hr class="border-gray-800">
                        <button onclick="logout()" class="block w-full text-left px-4 py-3 text-sm text-red-500 hover:bg-zinc-800 transition">
                            <i class="fas fa-sign-out-alt mr-2"></i> Sign Out
                        </button>
                    </div>
                </div>
            `;
        }
    } catch (e) {
        console.error("Failed to parse user data", e);
        localStorage.removeItem('user_data');
    }
});

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}