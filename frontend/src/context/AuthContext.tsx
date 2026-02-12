import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import type { AuthUser } from '@/types/auth';
import { authAPI, AUTH_TOKEN_KEY } from '@/services/api';

interface AuthContextType {
  user: AuthUser | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isInitializing: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const AUTH_STORAGE_KEY = 'face-r-auth-user';

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    const initialize = async () => {
      const token = localStorage.getItem(AUTH_TOKEN_KEY);
      const storedUser = localStorage.getItem(AUTH_STORAGE_KEY);

      if (!token || !storedUser) {
        setIsInitializing(false);
        return;
      }

      try {
        const me = await authAPI.me();
        setUser(me);
        localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(me));
      } catch {
        localStorage.removeItem(AUTH_TOKEN_KEY);
        localStorage.removeItem(AUTH_STORAGE_KEY);
      } finally {
        setIsInitializing(false);
      }
    };

    initialize();
  }, []);

  const login = async (username: string, password: string) => {
    const response = await authAPI.login(username.trim(), password);

    const nextUser: AuthUser = {
      id: response.user.id,
      username: response.user.username,
      role: response.user.role,
      is_active: response.user.is_active,
    };

    localStorage.setItem(AUTH_TOKEN_KEY, response.access_token);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem(AUTH_STORAGE_KEY);
    localStorage.removeItem(AUTH_TOKEN_KEY);
  };

  const value = useMemo(
    () => ({ user, login, logout, isAuthenticated: Boolean(user), isInitializing }),
    [user, isInitializing],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider');
  }
  return context;
};
