// Global State
let currentProducts = [];
let currentPage = 1;
let itemsPerPage = 12;
let currentEditingProduct = null;

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    if (api.getToken()) {
        showApp();
        loadData();
    } else {
        showAuth();
    }
});

// Auth Functions
function showAuth() {
    document.getElementById('auth-screen').style.display = 'flex';
    document.getElementById('app-screen').style.display = 'none';
}

function showApp() {
    document.getElementById('auth-screen').style.display = 'none';
    document.getElementById('app-screen').style.display = 'grid';
    
    const username = localStorage.getItem('current_user') || 'Usuario';
    document.getElementById('current-user').textContent = username;
}

function showLogin() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
}

function showRegister() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
}

async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    showLoading();
    
    try {
        await api.login(username, password);
        showToast('¡Bienvenido!', 'success');
        showApp();
        await loadData();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    showLoading();
    
    try {
        await api.register(username, email, password);
        showToast('Cuenta creada exitosamente. Por favor inicia sesión.', 'success');
        showLogin();
        
        // Pre-fill login form
        document.getElementById('login-username').value = username;
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function handleLogout() {
    api.removeToken();
    showToast('Sesión cerrada', 'info');
    showAuth();
}

// Navigation
function showSection(section) {
    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.closest('.nav-item').classList.add('active');
    
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.style.display = 'none';
    });
    
    // Show selected section
    const sectionMap = {
        'dashboard': 'dashboard-section',
        'products': 'products-section',
        'import-export': 'import-export-section'
    };
    
    document.getElementById(sectionMap[section]).style.display = 'block';
    
    // Update page title
    const titleMap = {
        'dashboard': 'Dashboard',
        'products': 'Productos',
        'import-export': 'Importar/Exportar'
    };
    
    document.getElementById('page-title').textContent = titleMap[section];
    
    // Load specific data for section
    if (section === 'import-export') {
        loadImportLogs();
    }
}

// Data Loading
async function loadData() {
    showLoading();
    
    try {
        await Promise.all([
            loadDashboardStats(),
            loadProducts()
        ]);
    } catch (error) {
        showToast('Error cargando datos', 'error');
    } finally {
        hideLoading();
    }
}

async function loadDashboardStats() {
    try {
        const response = await api.getProducts({ limit: 1000 });
        const products = response.items;
        
        // Calculate stats
        const totalProducts = response.total;
        const totalStock = products.reduce((sum, p) => sum + p.stock, 0);
        const totalValue = products.reduce((sum, p) => sum + (p.precio * p.stock), 0);
        const categories = [...new Set(products.map(p => p.categoria))].length;
        
        // Update stat cards
        document.getElementById('total-products').textContent = totalProducts;
        document.getElementById('total-stock').textContent = totalStock.toLocaleString();
        document.getElementById('total-value').textContent = '$' + totalValue.toLocaleString('es-ES', { minimumFractionDigits: 2 });
        document.getElementById('total-categories').textContent = categories;
        
        // Show recent products
        const recentProducts = products.slice(0, 5);
        displayRecentProducts(recentProducts);
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayRecentProducts(products) {
    const container = document.getElementById('recent-products-list');
    
    if (products.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:var(--secondary);padding:20px;">No hay productos recientes</p>';
        return;
    }
    
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-header">
                <div class="product-title">
                    <h3>${product.nombre}</h3>
                    <span class="product-category">${product.categoria}</span>
                </div>
            </div>
            <p class="product-description">${product.descripcion || 'Sin descripción'}</p>
            <div class="product-footer">
                <span class="product-price">$${product.precio.toFixed(2)}</span>
                <span class="product-stock ${product.stock < 10 ? 'low' : ''}">
                    <i class="fas fa-box"></i> ${product.stock} unidades
                </span>
            </div>
        </div>
    `).join('');
}

async function loadProducts(filters = {}) {
    showLoading();
    
    try {
        const params = {
            skip: (currentPage - 1) * itemsPerPage,
            limit: itemsPerPage,
            ...filters
        };
        
        const response = await api.getProducts(params);
        currentProducts = response.items;
        
        displayProducts(currentProducts);
        displayPagination(response.total);
        
        // Update category filter
        await updateCategoryFilter();
        
    } catch (error) {
        showToast('Error cargando productos', 'error');
    } finally {
        hideLoading();
    }
}

function displayProducts(products) {
    const container = document.getElementById('products-list');
    
    if (products.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:var(--secondary);padding:40px;">No se encontraron productos</p>';
        return;
    }
    
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-header">
                <div class="product-title">
                    <h3>${product.nombre}</h3>
                    <span class="product-category">${product.categoria}</span>
                </div>
                <div class="product-actions">
                    <button class="icon-btn edit" onclick="editProduct(${product.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="icon-btn delete" onclick="deleteProduct(${product.id})" title="Eliminar">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <p class="product-description">${product.descripcion || 'Sin descripción'}</p>
            <div class="product-footer">
                <span class="product-price">$${product.precio.toFixed(2)}</span>
                <span class="product-stock ${product.stock < 10 ? 'low' : ''}">
                    <i class="fas fa-box"></i> ${product.stock} unidades
                </span>
            </div>
        </div>
    `).join('');
}

function displayPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const container = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let html = `
        <button onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            <i class="fas fa-chevron-left"></i>
        </button>
    `;
    
    for (let i = 1; i <= Math.min(totalPages, 5); i++) {
        html += `
            <button onclick="changePage(${i})" ${i === currentPage ? 'class="active"' : ''}>
                ${i}
            </button>
        `;
    }
    
    if (totalPages > 5) {
        html += `<button disabled>...</button>`;
        html += `
            <button onclick="changePage(${totalPages})">
                ${totalPages}
            </button>
        `;
    }
    
    html += `
        <button onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            <i class="fas fa-chevron-right"></i>
        </button>
    `;
    
    container.innerHTML = html;
}

function changePage(page) {
    currentPage = page;
    loadProducts(getCurrentFilters());
}

async function updateCategoryFilter() {
    try {
        const response = await api.getProducts({ limit: 1000 });
        const categories = [...new Set(response.items.map(p => p.categoria))];
        
        const select = document.getElementById('category-filter');
        const currentValue = select.value;
        
        select.innerHTML = '<option value="">Todas las categorías</option>' +
            categories.map(cat => `<option value="${cat}">${cat}</option>`).join('');
        
        select.value = currentValue;
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function getCurrentFilters() {
    const filters = {};
    
    const categoria = document.getElementById('category-filter')?.value;
    const nombre = document.getElementById('search-input')?.value;
    const precioMin = document.getElementById('price-min')?.value;
    const precioMax = document.getElementById('price-max')?.value;
    
    if (categoria) filters.categoria = categoria;
    if (nombre) filters.nombre = nombre;
    if (precioMin) filters.precio_min = precioMin;
    if (precioMax) filters.precio_max = precioMax;
    
    return filters;
}

function searchProducts() {
    currentPage = 1;
    loadProducts(getCurrentFilters());
}

function filterProducts() {
    currentPage = 1;
    loadProducts(getCurrentFilters());
}

// Product Modal
function showProductModal(productId = null) {
    const modal = document.getElementById('product-modal');
    const form = document.getElementById('product-form');
    
    if (productId) {
        document.getElementById('modal-title').textContent = 'Editar Producto';
        loadProductToForm(productId);
    } else {
        document.getElementById('modal-title').textContent = 'Nuevo Producto';
        form.reset();
        currentEditingProduct = null;
    }
    
    modal.classList.add('show');
}

function closeProductModal() {
    document.getElementById('product-modal').classList.remove('show');
    document.getElementById('product-form').reset();
    currentEditingProduct = null;
}

async function loadProductToForm(productId) {
    try {
        const product = currentProducts.find(p => p.id === productId);
        
        if (!product) return;
        
        document.getElementById('product-nombre').value = product.nombre;
        document.getElementById('product-descripcion').value = product.descripcion || '';
        document.getElementById('product-precio').value = product.precio;
        document.getElementById('product-stock').value = product.stock;
        document.getElementById('product-categoria').value = product.categoria;
        
        currentEditingProduct = productId;
    } catch (error) {
        showToast('Error cargando producto', 'error');
    }
}

async function handleProductSubmit(event) {
    event.preventDefault();
    
    const productData = {
        nombre: document.getElementById('product-nombre').value,
        descripcion: document.getElementById('product-descripcion').value || null,
        precio: parseFloat(document.getElementById('product-precio').value),
        stock: parseInt(document.getElementById('product-stock').value),
        categoria: document.getElementById('product-categoria').value
    };
    
    showLoading();
    
    try {
        if (currentEditingProduct) {
            await api.updateProduct(currentEditingProduct, productData);
            showToast('Producto actualizado exitosamente', 'success');
        } else {
            await api.createProduct(productData);
            showToast('Producto creado exitosamente', 'success');
        }
        
        closeProductModal();
        await loadData();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function editProduct(productId) {
    showProductModal(productId);
}

async function deleteProduct(productId) {
    if (!confirm('¿Estás seguro de eliminar este producto?')) {
        return;
    }
    
    showLoading();
    
    try {
        await api.deleteProduct(productId);
        showToast('Producto eliminado exitosamente', 'success');
        await loadData();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Import/Export
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('import-btn').disabled = false;
    }
}

async function importProducts() {
    const fileInput = document.getElementById('import-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showToast('Por favor selecciona un archivo', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const result = await api.importProducts(file);
        
        const resultDiv = document.getElementById('import-result');
        resultDiv.className = 'import-result ' + (result.failed_rows > 0 ? 'error' : 'success');
        resultDiv.innerHTML = `
            <h3>${result.message}</h3>
            <p>Total: ${result.total_rows} | Exitosos: ${result.successful_rows} | Fallidos: ${result.failed_rows}</p>
        `;
        
        showToast('Importación completada', 'success');
        
        // Reset form
        fileInput.value = '';
        document.getElementById('file-name').textContent = '';
        document.getElementById('import-btn').disabled = true;
        
        await loadData();
        await loadImportLogs();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function exportProducts(format) {
    showLoading();
    
    try {
        await api.exportProducts(format);
        showToast('Archivo descargado exitosamente', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function loadImportLogs() {
    try {
        const response = await api.getImportLogs({ limit: 10 });
        displayImportLogs(response.items);
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

function displayImportLogs(logs) {
    const container = document.getElementById('import-logs');
    
    if (logs.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:var(--secondary);padding:20px;">No hay importaciones registradas</p>';
        return;
    }
    
    container.innerHTML = logs.map(log => `
        <div class="log-item">
            <div class="log-info">
                <h4>${log.filename}</h4>
                <p>Total: ${log.total_rows} | Exitosos: ${log.successful_rows} | Fallidos: ${log.failed_rows}</p>
                <p>${new Date(log.started_at).toLocaleString('es-ES')}</p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <span class="log-status ${log.status}">${log.status}</span>
                ${log.failed_rows > 0 ? `
                    <button class="btn btn-sm btn-danger" onclick="downloadErrors(${log.id})" title="Descargar errores">
                        <i class="fas fa-download"></i> Errores
                    </button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

async function downloadErrors(logId) {
    showLoading();
    
    try {
        await api.downloadImportErrors(logId);
        showToast('Archivo de errores descargado exitosamente', 'success');
    } catch (error) {
        showToast('Error al descargar archivo de errores', 'error');
    } finally {
        hideLoading();
    }
}
// UI Helpers
function showLoading() {
    document.getElementById('loading-overlay').classList.add('show');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.remove('show');
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconMap = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };
    
    toast.innerHTML = `
        <i class="fas ${iconMap[type]}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Close modal on click outside
window.onclick = function(event) {
    const modal = document.getElementById('product-modal');
    if (event.target === modal) {
        closeProductModal();
    }
}
