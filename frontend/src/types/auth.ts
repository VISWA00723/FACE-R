export type UserRole = 'admin' | 'user';

export interface AuthUser {
  id?: number;
  username: string;
  role: UserRole;
  is_active?: boolean;
}
