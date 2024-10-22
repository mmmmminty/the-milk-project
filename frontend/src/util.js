import { BACKEND_PORT } from "./config";

// TODO: Use in-memory storage for token
export function isValidToken(token) {}

export function setToken(token) {
  localStorage.setItem("token", token);
}
