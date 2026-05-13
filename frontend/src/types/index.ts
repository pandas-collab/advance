export interface User {
  id: string;
  email: string;
  name: string;
  isAdmin: boolean;
  createdAt: string;
}

export interface AgeCalculation {
  id: string;
  userId: string;
  birthDate: string;
  calculatedAt: string;
  results: AgeResults;
}

export interface AgeResults {
  years: number;
  months: number;
  days: number;
  hours: number;
  minutes: number;
  totalDays: number;
  totalHours: number;
  totalMinutes: number;
  nextBirthday: string;
  daysUntilBirthday: number;
  zodiacSign: string;
  lifeStage: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}
