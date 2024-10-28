export interface User {
  email: string;
  name: string;
  picture: string;
  sub: string; // Google's user ID
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (response: any) => void;
  logout: () => void;
}
