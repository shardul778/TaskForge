const API_BASE = import.meta.env.VITE_API_URL || "";

function getToken() {
  return localStorage.getItem("taskforge_token");
}

export function setToken(token) {
  if (token) {
    localStorage.setItem("taskforge_token", token);
  } else {
    localStorage.removeItem("taskforge_token");
  }
}

async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();

  if (token && !options.skipAuth) {
    headers.Authorization = `Bearer ${token}`;
  }

  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });

  let data = null;
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const detail = data?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg || d).join(", ")
          : `Request failed (${response.status})`;
    throw new Error(message);
  }

  return data;
}

export const api = {
  register: (username, email, password) =>
    request("/register", {
      method: "POST",
      skipAuth: true,
      body: JSON.stringify({ username, email, password }),
    }),

  login: (username, password) => {
    const form = new FormData();
    form.append("username", username);
    form.append("password", password);
    return request("/login", { method: "POST", skipAuth: true, body: form });
  },

  me: () => request("/me"),

  getProjects: () => request("/projects"),

  getProject: (id) => request(`/projects/${id}`),

  createProject: (name, description) =>
    request("/projects", {
      method: "POST",
      body: JSON.stringify({ name, description }),
    }),

  updateProject: (id, description) =>
    request(`/projects/${id}?description=${encodeURIComponent(description)}`, {
      method: "PUT",
    }),

  deleteProject: (id) => request(`/projects/${id}`, { method: "DELETE" }),

  getTasks: (projectId) => request(`/projects/${projectId}/tasks`),

  createTask: (projectId, title, description, priority) =>
    request(`/projects/${projectId}/tasks`, {
      method: "POST",
      body: JSON.stringify({ title, description, priority }),
    }),

  updateTask: (projectId, taskId, title, priority, description) => {
    const params = new URLSearchParams({ title, priority, description });
    return request(`/projects/${projectId}/tasks/${taskId}?${params}`, {
      method: "PUT",
    });
  },

  deleteTask: (projectId, taskId) =>
    request(`/projects/${projectId}/tasks/${taskId}`, { method: "DELETE" }),
};
