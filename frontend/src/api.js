export const login = async (username, password) => {
  const response = await fetch(`http://localhost:${BACKEND_PORT}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();

  if (data.error) {
    alert(data.error);
  }

  return data;
};
