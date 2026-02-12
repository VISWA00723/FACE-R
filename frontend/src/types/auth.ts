export type UserRole = 'admin' | 'user';

export interface AuthUser {
  username: string;
  role: UserRole;
}
