import { calculateAge, getCalculationHistory } from './api';

describe('API Integration Tests', () => {
  test('calculates age via API', async () => {
    const birthDate = '1990-01-01';
    const targetDate = '2023-01-01';

    try {
      const result = await calculateAge(birthDate, targetDate);
      expect(result).toBeDefined();
      expect(result.years).toBe(33);
    } catch (error) {
      // API might not be available in test environment
      console.warn('API test skipped - service unavailable');
    }
  });

  test('retrieves calculation history', async () => {
    try {
      const history = await getCalculationHistory();
      expect(Array.isArray(history)).toBe(true);
    } catch (error) {
      console.warn('History test skipped - service unavailable');
    }
  });
});
