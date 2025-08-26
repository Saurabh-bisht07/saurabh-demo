import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { jwtDecode } from 'jwt-decode';
import { authAPI } from '../services/api';

interface User {
  id: number;
  email: string;
  full_name: string;
  user_type: string;
  is_active: boolean;
  is_verified: boolean;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  phone: string;
  user_type: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing token on app load
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token) as any;
        const currentTime = Date.now() / 1000;
        
        if (decoded.exp > currentTime) {
          // Token is valid, set user
          setUser({
            id: decoded.user_id,
            email: decoded.sub,
            full_name: decoded.full_name || '',
            user_type: decoded.user_type,
            is_active: true,
            is_verified: true,
          });
        } else {
          // Token expired, remove it
          localStorage.removeItem('token');
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('token');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      
      const decoded = jwtDecode(access_token) as any;
      setUser({
        id: decoded.user_id,
        email: decoded.sub,
        full_name: decoded.full_name || '',
        user_type: decoded.user_type,
        is_active: true,
        is_verified: true,
      });
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      const response = await authAPI.register(userData);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      
      const decoded = jwtDecode(access_token) as any;
      setUser({
        id: decoded.user_id,
        email: decoded.sub,
        full_name: decoded.full_name || '',
        user_type: decoded.user_type,
        is_active: true,
        is_verified: true,
      });
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...userData });
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};