module.exports = {
  testEnvironment: 'node',
  testMatch: ['<rootDir>/src/**/*.integration.(js|jsx|ts|tsx)'],
  setupFilesAfterEnv: ['<rootDir>/src/setupIntegrationTests.js'],
  testTimeout: 30000
};
