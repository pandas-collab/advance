import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { ApiResponse, LoginRequest, RegisterRequest, AuthResponse, AgeCalculation, AgeResults } from '../types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const response: AxiosResponse<ApiResponse<AuthResponse>> = await this.api.post('/auth/login', credentials);
      if (response.data.success && response.data.data) {
        localStorage.setItem('token', response.data.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.data.user));
        return response.data.data;
      }
      throw new Error(response.data.message || 'Login failed');
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response: AxiosResponse<ApiResponse<AuthResponse>> = await this.api.post('/auth/register', userData);
      if (response.data.success && response.data.data) {
        return response.data.data;
      }
      throw new Error(response.data.message || 'Registration failed');
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  async logout(): Promise<void> {
    try {
      await this.api.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }

  // Age calculation endpoints
  async calculateAge(birthDate: string): Promise<AgeResults> {
    try {
      const response: AxiosResponse<ApiResponse<AgeResults>> = await this.api.post('/age/calculate', { birthDate });
      if (response.data.success && response.data.data) {
        return response.data.data;
      }
      throw new Error(response.data.message || 'Age calculation failed');
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Age calculation failed');
    }
  }

  async getCalculationHistory(): Promise<AgeCalculation[]> {
    try {
      const response: AxiosResponse<ApiResponse<AgeCalculation[]>> = await this.api.get('/age/history');
      if (response.data.success && response.data.data) {
        return response.data.data;
      }
      return [];
    } catch (error: any) {
      console.error('Failed to fetch calculation history:', error);
      return [];
    }
  }
}

export default new ApiService();
