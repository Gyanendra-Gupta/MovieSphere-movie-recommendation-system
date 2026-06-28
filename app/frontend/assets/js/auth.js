/**
 * MovieSphere Authentication Logic
 * Handles: Registration, Login, Form Validation, JWT Lifecycle
 */

const GENRES_LIST = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", 
    "Documentary", "Drama", "Family", "Fantasy", "Horror", 
    "Mystery", "Romance", "Sci-Fi", "Thriller"
];

document.addEventListener('DOMContentLoaded', () => {
    initGenreGrid();
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);

    const registerForm = document.getElementById('registerForm');
    if (registerForm) registerForm.addEventListener('submit', handleRegister);
});

function initGenreGrid() {
    const grid = document.getElementById('genreGrid');
    if (!grid) return;

    grid.innerHTML = GENRES_LIST.map(genre => `
        <label class="flex items-center p-2 rounded-lg border border-gray-800 cursor-pointer hover:bg-zinc-800 transition group">
            <input type="checkbox" name="genres" value="${genre}" class="hidden peer">
            <div class="w-4 h-4 rounded border border-gray-600 peer-checked:bg-red-600 peer-checked:border-red-600 flex items-center justify-center mr-2">
                <i class="fas fa-check text-[10px] text-white opacity-0 peer-checked:opacity-100"></i>
            </div>
            <span class="text-xs text-gray-400 peer-checked:text-white">${genre}</span>
        </label>
    `).join('');
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');

    // UI Feedback
    loginBtn.disabled = true;
    loginBtn.innerHTML = '<i class="fas fa-circle-notch animate-spin"></i>';

    const { data, ok } = await MovieSphereAPI.request('/auth/login', 'POST', { email, password });

    if (ok) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user_data', JSON.stringify(data.user));
        MovieSphereUI.showToast("Successfully logged in! Redirecting...");
        setTimeout(() => window.location.href = 'index.html', 1500);
    } else {
        MovieSphereUI.showToast(data.message || "Login failed", "error");
        loginBtn.disabled = false;
        loginBtn.innerHTML = 'Sign In';
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;
    
    const selectedGenres = Array.from(document.querySelectorAll('input[name="genres"]:checked'))
                                .map(el => el.value);

    // Validation
    if (password !== confirmPassword) {
        return MovieSphereUI.showToast("Passwords do not match", "error");
    }
    if (selectedGenres.length < 3) {
        return MovieSphereUI.showToast("Please select at least 3 genres", "error");
    }

    const registerBtn = document.getElementById('registerBtn');
    registerBtn.disabled = true;
    registerBtn.innerText = "Creating Account...";

    const { data, ok } = await MovieSphereAPI.request('/auth/register', 'POST', {
        name, email, password, confirm_password: confirmPassword, genres: selectedGenres
    });

    if (ok) {
        MovieSphereUI.showToast("Account created! You can now log in.");
        setTimeout(() => window.location.href = 'login.html', 2000);
    } else {
        MovieSphereUI.showToast(data.message || "Registration failed", "error");
        registerBtn.disabled = false;
        registerBtn.innerText = "Create My Account";
    }
}