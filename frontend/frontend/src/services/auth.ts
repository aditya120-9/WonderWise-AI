import api from "./api";

export interface AuthUser {
  id: number;
  email: string;
}

interface AuthResponse {
  access_token: string;
  user: AuthUser;
}

export async function authenticate(
  mode: "login" | "register",
  email: string,
  password: string,
) {
  const { data } = await api.post<AuthResponse>(`/auth/${mode}`, { email, password });
  localStorage.setItem("wonderwise_token", data.access_token);
  localStorage.setItem("wonderwise_user", JSON.stringify(data.user));
  return data.user;
}

export function getStoredUser(): AuthUser | null {
  const value = localStorage.getItem("wonderwise_user");
  return value ? (JSON.parse(value) as AuthUser) : null;
}

export function logout() {
  localStorage.removeItem("wonderwise_token");
  localStorage.removeItem("wonderwise_user");
}