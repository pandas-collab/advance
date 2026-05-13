// Integration test setup
process.env.NODE_ENV = 'test';
process.env.REACT_APP_API_URL = 'http://localhost:8000/api/v1';

// Global test timeout
jest.setTimeout(30000);
