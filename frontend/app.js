const API_BASE = {
    user: 'http://127.0.0.1:8001',
    product: 'http://127.0.0.1:8000',
    order: 'http://127.0.0.1:8002'
};

let currentUser = null;
let currentProductId = null;

// Auth Functions
function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
}

function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
}

async function register() {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch(`${API_BASE.user}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            showAlert('Registration successful! Please login.', 'success');
            showLogin();
        } else {
            showAlert(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showAlert('Error connecting to server', 'error');
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE.user}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            currentUser = { email, token: data.token };
            localStorage.setItem('user', JSON.stringify(currentUser));
            showMainContent();
            showAlert('Login successful!', 'success');
        } else {
            showAlert(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showAlert('Error connecting to server', 'error');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('user');
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('authButtons').style.display = 'block';
    document.getElementById('userInfo').style.display = 'none';
}

function showMainContent() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('mainContent').style.display = 'block';
    document.getElementById('authButtons').style.display = 'none';
    document.getElementById('userInfo').style.display = 'flex';
    document.getElementById('userEmail').textContent = currentUser.email;
    loadProducts();
}

// Tab Functions
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(`${tabName}Tab`).style.display = 'block';
    event.target.classList.add('active');

    if (tabName === 'products') loadProducts();
    if (tabName === 'orders') loadOrders();
}

// Product Functions
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE.product}/products`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        showAlert('Error loading products', 'error');
    }
}

async function searchProducts() {
    const searchTerm = document.getElementById('searchInput').value;
    
    try {
        const response = await fetch(`${API_BASE.product}/products/search?name=${searchTerm}`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        showAlert('Error searching products', 'error');
    }
}

function displayProducts(products) {
    const container = document.getElementById('productsList');
    
    if (!products || products.length === 0) {
        container.innerHTML = '<p>No products found</p>';
        return;
    }

    container.innerHTML = products.map(product => `
        <div class="product-card">
            <h3>${product.name}</h3>
            <p>${product.description || 'No description'}</p>
            <p class="price">$${product.price}</p>
            <p>Stock: ${product.quantity}</p>
            <button onclick="openOrderModal(${product.id}, '${product.name}', ${product.quantity})">
                Order Now
            </button>
        </div>
    `).join('');
}

async function addProduct() {
    const name = document.getElementById('productName').value;
    const description = document.getElementById('productDescription').value;
    const price = parseFloat(document.getElementById('productPrice').value);
    const quantity = parseInt(document.getElementById('productQuantity').value);

    try {
        const response = await fetch(`${API_BASE.product}/products/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify([{ name, description, price, quantity }])
        });

        if (response.ok) {
            showAlert('Product added successfully!', 'success');
            document.getElementById('productName').value = '';
            document.getElementById('productDescription').value = '';
            document.getElementById('productPrice').value = '';
            document.getElementById('productQuantity').value = '';
            loadProducts();
        } else {
            showAlert('Failed to add product', 'error');
        }
    } catch (error) {
        showAlert('Error adding product', 'error');
    }
}

// Order Functions
function openOrderModal(productId, productName, maxQuantity) {
    currentProductId = productId;
    document.getElementById('orderProductName').textContent = `Product: ${productName}`;
    document.getElementById('orderQuantity').max = maxQuantity;
    document.getElementById('orderModal').style.display = 'block';
}

function closeOrderModal() {
    document.getElementById('orderModal').style.display = 'none';
    document.getElementById('orderQuantity').value = '';
}

async function placeOrder() {
    const quantity = parseInt(document.getElementById('orderQuantity').value);

    if (!quantity || quantity <= 0) {
        showAlert('Please enter a valid quantity', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE.order}/order`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id: currentProductId,
                quantity: quantity
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('Order placed successfully!', 'success');
            closeOrderModal();
            loadProducts();
        } else {
            showAlert(data.detail || 'Failed to place order', 'error');
        }
    } catch (error) {
        showAlert('Error placing order', 'error');
    }
}

async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE.order}/orders`);
        const orders = await response.json();
        displayOrders(orders);
    } catch (error) {
        showAlert('Error loading orders', 'error');
    }
}

function displayOrders(orders) {
    const container = document.getElementById('ordersList');
    
    if (!orders || orders.length === 0) {
        container.innerHTML = '<p>No orders found</p>';
        return;
    }

    container.innerHTML = orders.map(order => `
        <div class="order-card">
            <h3>Order #${order.id}</h3>
            <p>Product ID: ${order.product_id}</p>
            <p>Quantity: ${order.quantity}</p>
            <span class="status">${order.status}</span>
        </div>
    `).join('');
}

// Utility Functions
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 3000);
}

// Check for saved user on load
window.onload = function() {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        showMainContent();
    }
};
