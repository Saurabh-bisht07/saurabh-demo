import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API interfaces
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  phone: string;
  user_type: string;
}

export interface DonorCreateRequest {
  blood_group: string;
  can_donate_blood: boolean;
  can_donate_organs: boolean;
  organs_available?: string;
  latitude: number;
  longitude: number;
  city: string;
  state: string;
  country: string;
  age: number;
  weight?: number;
  height?: number;
  medical_conditions?: string;
  medications?: string;
  is_available: boolean;
  availability_notes?: string;
}

export interface DonorSearchRequest {
  blood_group: string;
  request_type: string;
  organ_needed?: string;
  latitude: number;
  longitude: number;
  radius_km: number;
  max_results: number;
}

export interface RequestCreateRequest {
  request_type: string;
  blood_group: string;
  organ_needed?: string;
  latitude: number;
  longitude: number;
  city: string;
  state: string;
  country: string;
  urgency_level: string;
  required_by_date?: string;
  description?: string;
  contact_person: string;
  contact_phone: string;
  hospital_name?: string;
}

// API service functions
export const authAPI = {
  login: (email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/login', { email, password });
  },

  register: (userData: RegisterRequest): Promise<AxiosResponse> => {
    return api.post('/api/auth/register', userData);
  },
};

export const donorAPI = {
  register: (donorData: DonorCreateRequest): Promise<AxiosResponse> => {
    return api.post('/api/donors/register', donorData);
  },

  search: (searchParams: DonorSearchRequest): Promise<AxiosResponse> => {
    const params = new URLSearchParams();
    Object.entries(searchParams).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, value.toString());
      }
    });
    return api.get(`/api/donors/search?${params.toString()}`);
  },

  getProfile: (): Promise<AxiosResponse> => {
    return api.get('/api/donors/profile');
  },

  updateProfile: (donorData: Partial<DonorCreateRequest>): Promise<AxiosResponse> => {
    return api.put('/api/donors/profile', donorData);
  },

  getStats: (): Promise<AxiosResponse> => {
    return api.get('/api/donors/stats');
  },
};

export const requestAPI = {
  create: (requestData: RequestCreateRequest): Promise<AxiosResponse> => {
    return api.post('/api/requests/create', requestData);
  },

  getMyRequests: (): Promise<AxiosResponse> => {
    return api.get('/api/requests/my-requests');
  },

  search: (params: any): Promise<AxiosResponse> => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, value.toString());
      }
    });
    return api.get(`/api/requests/search?${searchParams.toString()}`);
  },

  getById: (id: number): Promise<AxiosResponse> => {
    return api.get(`/api/requests/${id}`);
  },

  update: (id: number, requestData: Partial<RequestCreateRequest>): Promise<AxiosResponse> => {
    return api.put(`/api/requests/${id}`, requestData);
  },

  match: (id: number, donorId: number): Promise<AxiosResponse> => {
    return api.post(`/api/requests/${id}/match`, { donor_id: donorId });
  },

  complete: (id: number): Promise<AxiosResponse> => {
    return api.post(`/api/requests/${id}/complete`);
  },
};

export const notificationAPI = {
  getHistory: (limit?: number, offset?: number): Promise<AxiosResponse> => {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    if (offset) params.append('offset', offset.toString());
    return api.get(`/api/notifications/history?${params.toString()}`);
  },

  getUnreadCount: (): Promise<AxiosResponse> => {
    return api.get('/api/notifications/unread-count');
  },

  markAsRead: (id: number): Promise<AxiosResponse> => {
    return api.post(`/api/notifications/${id}/mark-read`);
  },

  markAllAsRead: (): Promise<AxiosResponse> => {
    return api.post('/api/notifications/mark-all-read');
  },
};

export const adminAPI = {
  getDashboard: (): Promise<AxiosResponse> => {
    return api.get('/api/admin/dashboard');
  },

  getRequestAnalytics: (days?: number): Promise<AxiosResponse> => {
    const params = days ? `?days=${days}` : '';
    return api.get(`/api/admin/analytics/requests${params}`);
  },

  getDonorAnalytics: (): Promise<AxiosResponse> => {
    return api.get('/api/admin/analytics/donors');
  },

  trainMLModel: (): Promise<AxiosResponse> => {
    return api.post('/api/admin/ml/train');
  },

  updateDonorReliability: (): Promise<AxiosResponse> => {
    return api.post('/api/admin/donors/update-reliability');
  },

  getAllUsers: (limit?: number, offset?: number): Promise<AxiosResponse> => {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    if (offset) params.append('offset', offset.toString());
    return api.get(`/api/admin/users?${params.toString()}`);
  },

  getAllRequests: (status?: string, limit?: number, offset?: number): Promise<AxiosResponse> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (limit) params.append('limit', limit.toString());
    if (offset) params.append('offset', offset.toString());
    return api.get(`/api/admin/requests?${params.toString()}`);
  },
};

export default api;