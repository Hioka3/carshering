let currentUser = null;

function showHomepage() {
    document.getElementById('homepage').style.display = 'block';
    document.getElementById('auth-page').style.display = 'none';
    document.getElementById('register-page').style.display = 'none';
    document.getElementById('main-app').style.display = 'none';
}

function showAuth() {
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('auth-page').style.display = 'block';
    document.getElementById('register-page').style.display = 'none';
    document.getElementById('main-app').style.display = 'none';
}

function showRegisterPage() {
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('auth-page').style.display = 'none';
    document.getElementById('register-page').style.display = 'block';
    document.getElementById('main-app').style.display = 'none';
}

function showMainApp() {
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('auth-page').style.display = 'none';
    document.getElementById('register-page').style.display = 'none';
    document.getElementById('main-app').style.display = 'block';
    
    document.getElementById('user-greeting').textContent = ` Добро пожаловать, ${currentUser.username}!`;
    
    loadCars();
    loadOrders();
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showNotification('Заполните все поля', 'error');
        return;
    }
    
    fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            currentUser = data.user;
            showMainApp();
            showNotification('Вход выполнен успешно!', 'success');
        } else {
            showNotification('Неверные учетные данные', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    });
}

function register() {
    const username = document.getElementById('reg_username').value;
    const password = document.getElementById('reg_password').value;
    const email = document.getElementById('reg_email').value;
    
    if (!username || !password || !email) {
        showNotification('Заполните все поля', 'error');
        return;
    }
    
    fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password, email})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification('Регистрация успешна! Теперь войдите в аккаунт', 'success');
            showAuth();
            document.getElementById('reg_username').value = '';
            document.getElementById('reg_password').value = '';
            document.getElementById('reg_email').value = '';
        } else {
            showNotification('Ошибка регистрации', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    });
}

function logout() {
    currentUser = null;
    showHomepage();
    showNotification('Вы вышли из аккаунта', 'info');
}

function loadCars() {
    const carsContainer = document.getElementById('cars');
    carsContainer.innerHTML = '<div class="loading"> Загрузка машин...</div>';
    
    fetch('http://localhost:5000/api/cars')
    .then(res => res.json())
    .then(data => {
        carsContainer.innerHTML = '';
        if (data.cars && data.cars.length > 0) {
            data.cars.forEach(car => {
                const carCard = createCarCard(car);
                carsContainer.appendChild(carCard);
            });
        } else {
            carsContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>Нет доступных машин</p></div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        carsContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>Ошибка загрузки машин</p></div>';
    });
}

function createCarCard(car) {
    const card = document.createElement('div');
    card.className = 'car-card';
    
    const statusClass = car.status === 'available' ? 'status-available' : 'status-booked';
    const statusText = car.status === 'available' ? ' ДОСТУПНА' : ' ЗАБРОНИРОВАНА';
    
    card.innerHTML = `
        <div class="car-image">
            ${car.image_url ? `<img src="${car.image_url}" alt="${car.model}" onerror="this.style.display='none'; this.parentNode.innerHTML='';">` : ''}
        </div>
        <div class="car-details">
            <h3> ${car.model}</h3>
            <div class="car-info">
                <span>Номер: ${car.number}</span>
                <span>Цена: ${car.price_per_hour} ₽/час</span>
            </div>
            <div class="car-status ${statusClass}">${statusText}</div>
            ${car.status === 'available' ? 
                `<button class="book-btn" onclick="bookCar(${car.id})"> ЗАБРОНИРОВАТЬ</button>` : 
                `<button class="book-btn" disabled>Недоступно</button>`
            }
        </div>
    `;
    
    return card;
}

function bookCar(carId) {
    fetch('http://localhost:5000/api/book', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: currentUser.id, car_id: carId})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification('Машина успешно забронирована!', 'success');
            loadCars();
            loadOrders();
        } else {
            showNotification('Ошибка бронирования', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    });
}

function loadOrders() {
    const ordersContainer = document.getElementById('orders');
    ordersContainer.innerHTML = '<div class="loading"> Загрузка заказов...</div>';
    
    fetch(`http://localhost:5000/api/orders?user_id=${currentUser.id}`)
    .then(res => res.json())
    .then(data => {
        ordersContainer.innerHTML = '';
        if (data.orders && data.orders.length > 0) {
            data.orders.forEach(order => {
                const orderCard = createOrderCard(order);
                ordersContainer.appendChild(orderCard);
            });
        } else {
            ordersContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>У вас пока нет заказов</p></div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        ordersContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>Ошибка загрузки заказов</p></div>';
    });
}

function createOrderCard(order) {
    const card = document.createElement('div');
    card.className = 'order-card';
    
    const statusClass = order.status === 'active' ? 'status-active' : 'status-completed';
    const statusText = order.status === 'active' ? 'АКТИВЕН' : 'ЗАВЕРШЕН';
    
    const startTime = new Date(order.start_time).toLocaleString('ru-RU');
    const endTime = order.end_time ? new Date(order.end_time).toLocaleString('ru-RU') : 'В процессе';
    
    card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3> ${order.model}</h3>
            <span class="order-status ${statusClass}">${statusText}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; opacity: 0.8;">
            <div> Начало: ${startTime}</div>
            <div> Конец: ${endTime}</div>
        </div>
    `;
    
    return card;
}


function showNotification(message, type = 'info') {
 
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        transition: all 0.3s ease;
        color: #333;
        font-weight: 500;
        border-left: 4px solid ${type === 'success' ? '#4cd964' : type === 'error' ? '#ff6b6b' : '#ffcc00'};
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    showHomepage();
    
    document.getElementById('password').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            login();
        }
    });
    
    document.getElementById('reg_password').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            register();
        }
    });
});

let allCars = [];


function loadCarsWithFilters() {
    const carsContainer = document.getElementById('cars');
    carsContainer.innerHTML = '<div class="loading"> Загрузка машин...</div>';
    
    fetch('http://localhost:5000/api/cars')
    .then(res => res.json())
    .then(data => {
        if (data.cars && data.cars.length > 0) {
            allCars = data.cars;
            displayCars(allCars);
        } else {
            carsContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>Нет доступных машин</p></div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        carsContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>Ошибка загрузки машин</p></div>';
    });
}

function displayCars(cars) {
    const carsContainer = document.getElementById('cars');
    carsContainer.innerHTML = '';
    
    if (cars.length > 0) {
        cars.forEach(car => {
            const carCard = createCarCard(car);
            carsContainer.appendChild(carCard);
        });
    } else {
        carsContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon"></div><p>Нет машин по выбранным фильтрам</p></div>';
    }
}

function applyFilters() {
    const priceFilter = document.getElementById('price-filter').value;
    const statusFilter = document.getElementById('status-filter').value;
    const modelFilter = document.getElementById('model-filter').value.toLowerCase();
    
    let filteredCars = allCars;
    
    if (priceFilter !== 'all') {
        filteredCars = filteredCars.filter(car => {
            const price = parseFloat(car.price_per_hour);
            switch (priceFilter) {
                case '0-10':
                    return price >= 0 && price <= 10;
                case '10-15':
                    return price > 10 && price <= 15;
                case '15-20':
                    return price > 15 && price <= 20;
                case '20+':
                    return price > 20;
                default:
                    return true;
            }
        });
    }
    
    if (statusFilter !== 'all') {
        filteredCars = filteredCars.filter(car => car.status === statusFilter);
    }
    
    if (modelFilter.trim() !== '') {
        filteredCars = filteredCars.filter(car => 
            car.model.toLowerCase().includes(modelFilter)
        );
    }
    
    displayCars(filteredCars);
}

function resetFilters() {
    document.getElementById('price-filter').value = 'all';
    document.getElementById('status-filter').value = 'all';
    document.getElementById('model-filter').value = '';
    displayCars(allCars);
}

function loadCars() {
    loadCarsWithFilters();
}
