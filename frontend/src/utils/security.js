// Security utilities for frontend
export const securityConfig = {
  // Content Security Policy helpers
  validateInput: (input) => {
    if (typeof input !== 'string') return false;
    // Basic XSS prevention
    const xssPattern = /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi;
    return !xssPattern.test(input);
  },

  // Sanitize user input
  sanitizeInput: (input) => {
    if (typeof input !== 'string') return input;
    return input
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  },

  // Environment variable validation
  validateEnvironment: () => {
    const requiredEnvVars = ['REACT_APP_API_URL'];
    const missing = requiredEnvVars.filter(varName => !process.env[varName]);

    if (missing.length > 0) {
      console.warn('Missing environment variables:', missing);
    }

    return missing.length === 0;
  }
};

// Initialize security checks
securityConfig.validateEnvironment();
