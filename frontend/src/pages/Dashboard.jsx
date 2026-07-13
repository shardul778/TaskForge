import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import Layout from "../components/Layout";

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", description: "" });

  const loadProjects = async () => {
    try {
      const data = await api.getProjects();
      setProjects(data.project || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.createProject(form.name.trim(), form.description.trim());
      setForm({ name: "", description: "" });
      setShowForm(false);
      await loadProjects();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this project?")) return;
    try {
      await api.deleteProject(id);
      await loadProjects();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Projects</h1>
          <p className="muted">Select a project to manage its tasks</p>
        </div>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => setShowForm((v) => !v)}
        >
          {showForm ? "Cancel" : "+ New project"}
        </button>
      </div>

      {error && <div className="alert error">{error}</div>}

      {showForm && (
        <form className="card form-inline" onSubmit={handleCreate}>
          <label>
            Name
            <input
              value={form.name}
              onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
              required
            />
          </label>
          <label>
            Description
            <textarea
              rows={2}
              value={form.description}
              onChange={(e) =>
                setForm((p) => ({ ...p, description: e.target.value }))
              }
              required
            />
          </label>
          <button type="submit" className="btn btn-primary">
            Create project
          </button>
        </form>
      )}

      {loading ? (
        <p className="muted">Loading projects...</p>
      ) : projects.length === 0 ? (
        <div className="empty card">
          <h3>No projects yet</h3>
          <p className="muted">Create your first project to get started.</p>
        </div>
      ) : (
        <div className="grid">
          {projects.map((project) => (
            <article key={project.id} className="card project-card">
              <div>
                <h3>{project.name}</h3>
                <p className="muted">{project.description}</p>
              </div>
              <div className="card-actions">
                <Link
                  to={`/projects/${project.id}`}
                  className="btn btn-primary"
                >
                  Open
                </Link>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={() => handleDelete(project.id)}
                >
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </Layout>
  );
}
