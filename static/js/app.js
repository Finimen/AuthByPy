const API_BASE = '/api/auth';
let currentToken = localStorage.getItem('authToken');

// Показ секций
function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionName + '-section').classList.add('active');
    
    // Обновляем навигацию
    document.querySelectorAll('.nav button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Показ сообщений
function showMessage(elementId, message, type = 'success') {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `message ${type}`;
    element.style.display = 'block';
    
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Регистрация
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('register-username').value,
        email: document.getElementById('register-email').value,
        password: document.getElementById('register-password').value
    };
    
    try {
        const response = await fetch(API_BASE + '/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('register-message', 'Registration successful! Please login.', 'success');
            document.getElementById('register-form').reset();
            showSection('login');
        } else {
            showMessage('register-message', data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('register-message', 'Network error: ' + error.message, 'error');
    }
});

// Логин
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('login-username').value,
        password: document.getElementById('login-password').value
    };
    
    try {
        const response = await fetch(API_BASE + '/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentToken = data.access_token;
            localStorage.setItem('authToken', currentToken);
            showMessage('login-message', 'Login successful!', 'success');
            document.getElementById('login-form').reset();
            updateUserInfo();
            showSection('home');
        } else {
            showMessage('login-message', data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('login-message', 'Network error: ' + error.message, 'error');
    }
});

// Логаут
async function logout() {
    try {
        if (currentToken) {
            await fetch(API_BASE + '/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            });
        }
        
        currentToken = null;
        localStorage.removeItem('authToken');
        document.getElementById('user-info').classList.add('hidden');
        showMessage('login-message', 'Logged out successfully', 'success');
        showSection('home');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Обновление информации о пользователе
async function updateUserInfo() {
    if (currentToken) {
        document.getElementById('user-info').classList.remove('hidden');
        document.getElementById('user-details').textContent = `Logged in with token: ${currentToken.substring(0, 20)}...`;
    }
}

// Проверяем токен при загрузке
document.addEventListener('DOMContentLoaded', () => {
    if (currentToken) {
        updateUserInfo();
    }
});