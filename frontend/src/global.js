import { BACKEND_PORT } from "./config";
import { isUserLoggedIn, setToken } from "./util";
import { login } from "./api";

document
  .getElementById("login-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const data = await login(username, password);

    if (data.token) {
      setToken(data.token);
    }

    if (isUserLoggedIn()) {
      window.location.href = "/dashboard";
    }
  });
