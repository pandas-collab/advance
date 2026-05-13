// Admin-related type definitions and constants

export const ValidationRuleTypes = {
    REQUIRED: 'required',
    MIN_VALUE: 'min_value',
    MAX_VALUE: 'max_value',
    PATTERN: 'pattern',
    CUSTOM: 'custom'
};

export const APIKeyScopes = {
    READ: 'read',
    WRITE: 'write',
    ADMIN: 'admin'
};

export const ConfigSections = {
    CALCULATION: 'calculation',
    VALIDATION: 'validation',
    SECURITY: 'security',
    FEATURES: 'features'
};

// Helper functions for type checking
export const isValidRule = (rule) => {
    return rule && typeof rule === 'object' && rule.type && rule.field;
};

export const isValidAPIKey = (key) => {
    return key && typeof key === 'object' && key.name && key.scope;
};
