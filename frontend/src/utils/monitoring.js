// System monitoring utilities
export const healthCheck = {
  checkApiHealth: async () => {
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  },

  checkLocalStorage: () => {
    try {
      localStorage.setItem('test', 'test');
      localStorage.removeItem('test');
      return true;
    } catch (error) {
      return false;
    }
  },

  getSystemStatus: async () => {
    const status = {
      api: await healthCheck.checkApiHealth(),
      localStorage: healthCheck.checkLocalStorage(),
      timestamp: new Date().toISOString()
    };

    console.log('System Status:', status);
    return status;
  }
};

// Logging utilities
export const logger = {
  info: (message, data) => {
    console.log(`[INFO] ${message}`, data || '');
  },

  error: (message, error) => {
    console.error(`[ERROR] ${message}`, error || '');
  },

  warn: (message, data) => {
    console.warn(`[WARN] ${message}`, data || '');
  }
};
