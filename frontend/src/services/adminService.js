// Admin service for API calls
const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000/api/v1';

export const adminService = {
    // Validation rules management
    async getValidationRules() {
        const response = await fetch(`${API_BASE}/admin/validation-rules`);
        return response.json();
    },

    async createValidationRule(rule) {
        const response = await fetch(`${API_BASE}/admin/validation-rules`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(rule)
        });
        return response.json();
    },

    // API key management
    async getAPIKeys() {
        const response = await fetch(`${API_BASE}/admin/api-keys`);
        return response.json();
    },

    async generateAPIKey(keyData) {
        const response = await fetch(`${API_BASE}/admin/api-keys`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(keyData)
        });
        return response.json();
    },

    // Configuration management
    async getConfig() {
        const response = await fetch(`${API_BASE}/admin/config`);
        return response.json();
    },

    async updateConfig(config) {
        const response = await fetch(`${API_BASE}/admin/config`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        return response.json();
    }
};

export default adminService;
