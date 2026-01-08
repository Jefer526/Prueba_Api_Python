// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// API Helper Functions
const api = {
    // Get token from localStorage
    getToken() {
        return localStorage.getItem('access_token');
    },

    // Set token in localStorage
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    // Remove token from localStorage
    removeToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('current_user');
    },

    // Get headers with authentication
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (includeAuth && this.getToken()) {
            headers['Authorization'] = `Bearer ${this.getToken()}`;
        }

        return headers;
    },

    // Handle API response
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Error en la petición');
        }
        return response.json();
    },

    // Generic GET request
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'GET',
                headers: this.getHeaders(),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('GET Error:', error);
            throw error;
        }
    },

    // Generic POST request
    async post(endpoint, data, includeAuth = true) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(includeAuth),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('POST Error:', error);
            throw error;
        }
    },

    // Generic PUT request
    async put(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('PUT Error:', error);
            throw error;
        }
    },

    // Generic DELETE request
    async delete(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'DELETE',
                headers: this.getHeaders(),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('DELETE Error:', error);
            throw error;
        }
    },

    // Login with form data
    async login(username, password) {
        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || 'Credenciales incorrectas');
            }

            const data = await response.json();
            this.setToken(data.access_token);
            localStorage.setItem('current_user', username);
            return data;
        } catch (error) {
            console.error('Login Error:', error);
            throw error;
        }
    },

    // Register user
    async register(username, email, password) {
        return await this.post('/auth/register', { username, email, password }, false);
    },

    // Get products with filters
    async getProducts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return await this.get(`/products?${queryString}`);
    },

    // Get single product
    async getProduct(id) {
        return await this.get(`/products/${id}`);
    },

    // Create product
    async createProduct(productData) {
        return await this.post('/products', productData);
    },

    // Update product
    async updateProduct(id, productData) {
        return await this.put(`/products/${id}`, productData);
    },

    // Delete product
    async deleteProduct(id) {
        return await this.delete(`/products/${id}`);
    },

    // Import products
    async importProducts(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/products/import`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.getToken()}`,
                },
                body: formData,
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Import Error:', error);
            throw error;
        }
    },

    // Export products
    async exportProducts(format = 'csv') {
        try {
            const response = await fetch(`${API_BASE_URL}/products/export/${format}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.getToken()}`,
                },
            });

            if (!response.ok) {
                throw new Error('Error al exportar');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `productos_export.${format === 'csv' ? 'csv' : 'xlsx'}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Export Error:', error);
            throw error;
        }
    },

    // Get import logs
    async getImportLogs(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return await this.get(`/products/import-logs?${queryString}`);
    }
};
