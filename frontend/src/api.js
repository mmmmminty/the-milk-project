import { BACKEND_PORT } from "./config";
import { getToken } from "./util";

const apiRequest = async (url, method, body = null) => {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      authorization: getToken(),
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const data = await response.json();

  if (data.error) {
    alert(data.error);
  }

  return data;
};

const get = (url) => apiRequest(url, "GET");
const post = (url, body) => apiRequest(url, "POST", body);
const put = (url, body) => apiRequest(url, "PUT", body);
const del = (url) => apiRequest(url, "DELETE");

export const login = async (username, password) => {
  const url = `http://localhost:${BACKEND_PORT}/login`;
  return await post(url, { username, password });
};

export const getMilk = async (milkId) => {
  const url = `http://localhost:${BACKEND_PORT}/milk?id=${milkId}`;
  return await get(url);
};
