export interface IUser {
  user_id: string;
  email: string;
  full_name: string;
  is_admin: boolean;
}

export interface IAuthResponse {
  user_id: string;
  email: string;
  access_token: string;
  token_type: string;
}

export interface ICalculationRequest {
  birth_date: string;
  target_date: string;
  precision_level: string;
}

export interface ICalculationResult {
  calculation_id: string;
  years: number;
  months: number;
  days: number;
  total_days: number;
  created_at: string;
}

export interface ICalculation extends ICalculationResult {
  birth_date: string;
  target_date: string;
}

export interface ILoginRequest {
  email: string;
  password: string;
}

export interface IRegisterRequest {
  email: string;
  password: string;
  full_name: string;
}
