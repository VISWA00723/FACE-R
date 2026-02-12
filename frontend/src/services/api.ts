/**
 * API service for backend communication
 */
import axios from 'axios';
import type {
  Employee,
  EmployeeCreate,
  AttendanceTodayResponse,
  AttendanceHistoryResponse,
  FaceRecognitionResponse,
  AttendanceStats,
} from '@/types';
import type { AuthUser } from '@/types/auth';

// Use relative URL when VITE_API_URL is not set (works with proxy)
const API_BASE_URL = import.meta.env.VITE_API_URL || '';
const API_V1 = API_BASE_URL ? `${API_BASE_URL}/api/v1` : '/api/v1';

export const AUTH_TOKEN_KEY = 'face-r-auth-token';

// Create axios instance
const api = axios.create({
  baseURL: API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: number;
    username: string;
    role: 'admin' | 'user';
    is_active: boolean;
    created_at: string;
  };
}

export const authAPI = {
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/login', { username, password });
    return response.data;
  },

  me: async (): Promise<AuthUser> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Employee APIs
export const employeeAPI = {
  // Register new employee
  register: async (data: EmployeeCreate): Promise<Employee> => {
    const response = await api.post<Employee>('/register_employee', data);
    return response.data;
  },

  // Get all employees
  getAll: async (skip = 0, limit = 100): Promise<{ total: number; employees: Employee[] }> => {
    const response = await api.get('/employees', { params: { skip, limit } });
    return response.data;
  },

  // Get employee by ID
  getById: async (employeeId: string): Promise<Employee> => {
    const response = await api.get<Employee>(`/employees/${employeeId}`);
    return response.data;
  },

  // Delete employee
  delete: async (employeeId: string): Promise<void> => {
    await api.delete(`/employees/${employeeId}`);
  },
};

// Face Recognition APIs
export const recognitionAPI = {
  // Recognize face
  recognize: async (image: string): Promise<FaceRecognitionResponse> => {
    const response = await api.post<FaceRecognitionResponse>('/recognize_face', { image });
    return response.data;
  },

  // Detect face (testing)
  detect: async (image: string): Promise<{ face_detected: boolean; num_faces?: number; message: string }> => {
    const response = await api.post('/detect_face', { image });
    return response.data;
  },
};

// Attendance APIs
export const attendanceAPI = {
  // Get today's attendance
  getToday: async (): Promise<AttendanceTodayResponse> => {
    const response = await api.get<AttendanceTodayResponse>('/attendance_today');
    return response.data;
  },

  // Get attendance history
  getHistory: async (params?: {
    start_date?: string;
    end_date?: string;
    employee_id?: string;
    limit?: number;
    offset?: number;
  }): Promise<AttendanceHistoryResponse> => {
    const response = await api.get<AttendanceHistoryResponse>('/attendance_history', { params });
    return response.data;
  },

  // Get attendance statistics
  getStats: async (start_date?: string, end_date?: string): Promise<AttendanceStats> => {
    const response = await api.get<AttendanceStats>('/attendance_stats', {
      params: { start_date, end_date },
    });
    return response.data;
  },

  // Export attendance
  exportCSV: async (params?: {
    start_date?: string;
    end_date?: string;
    employee_id?: string;
  }): Promise<Blob> => {
    const response = await api.get('/attendance_export', {
      params,
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
