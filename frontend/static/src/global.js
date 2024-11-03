import { getToken } from "./util";
import { login } from "./api";

console.log("Global JS loaded");

document.getElementById("login-btn").addEventListener("click", (event) => {
  event.preventDefault();

  console.log("Logging in...");

  login(username, password);

  if (getToken() !== null) {
    window.location.href = "/scanner.html";
  }
});
