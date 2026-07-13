import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import Layout from "../components/Layout";

export default function ProjectDetail() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [form, setForm] = useState({
    title: "",
    description: "",
    priority: "medium",
  });
  const [editDescription, setEditDescription] = useState("");

  const loadData = async () => {
    setLoading(true);
    setError("");
    try {
      const [projectData, tasksData] = await Promise.all([
        api.getProject(projectId),
        api.getTasks(projectId),
      ]);
      setProject(projectData.project);
      setEditDescription(projectData.project.description || "");
      setTasks(tasksData.project || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [projectId]);

  const resetTaskForm = () => {
    setForm({ title: "", description: "", priority: "medium" });
    setEditingTask(null);
    setShowForm(false);
  };

  const handleTaskSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (editingTask) {
        await api.updateTask(
          projectId,
          editingTask.id,
          form.title.trim(),
          form.priority,
          form.description.trim()
        );
      } else {
        await api.createTask(
          projectId,
          form.title.trim(),
          form.description.trim(),
          form.priority
        );
      }
      resetTaskForm();
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const startEditTask = (task) => {
    setEditingTask(task);
    setForm({
      title: task.title,
      description: task.description || "",
      priority: task.priority || "medium",
    });
    setShowForm(true);
  };

  const handleDeleteTask = async (taskId) => {
    if (!confirm("Delete this task?")) return;
    try {
      await api.deleteTask(projectId, taskId);
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateProject = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.updateProject(projectId, editDescription.trim());
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return (
      <Layout>
        <p className="muted">Loading project...</p>
      </Layout>
    );
  }

  if (!project) {
    return (
      <Layout>
        <div className="alert error">Project not found.</div>
        <Link to="/dashboard" className="btn btn-ghost">
          Back to projects
        </Link>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="breadcrumb">
        <Link to="/dashboard">Projects</Link>
        <span>/</span>
        <span>{project.name}</span>
      </div>

      {error && <div className="alert error">{error}</div>}

      <section className="card project-detail">
        <h1>{project.name}</h1>
        <form className="form" onSubmit={handleUpdateProject}>
          <label>
            Description
            <textarea
              rows={3}
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              required
            />
          </label>
          <button type="submit" className="btn btn-ghost">
            Save description
          </button>
        </form>
      </section>

      <div className="page-header">
        <h2>Tasks</h2>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => {
            if (showForm && !editingTask) {
              resetTaskForm();
            } else {
              setEditingTask(null);
              setForm({ title: "", description: "", priority: "medium" });
              setShowForm(true);
            }
          }}
        >
          {showForm ? "Cancel" : "+ Add task"}
        </button>
      </div>

      {showForm && (
        <form className="card form" onSubmit={handleTaskSubmit}>
          <h3>{editingTask ? "Edit task" : "New task"}</h3>
          <label>
            Title
            <input
              value={form.title}
              onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))}
              required
            />
          </label>
          <label>
            Description
            <textarea
              rows={3}
              value={form.description}
              onChange={(e) =>
                setForm((p) => ({ ...p, description: e.target.value }))
              }
              required
            />
          </label>
          <label>
            Priority
            <select
              value={form.priority}
              onChange={(e) =>
                setForm((p) => ({ ...p, priority: e.target.value }))
              }
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </label>
          <button type="submit" className="btn btn-primary">
            {editingTask ? "Update task" : "Create task"}
          </button>
        </form>
      )}

      {tasks.length === 0 ? (
        <div className="empty card">
          <p className="muted">No tasks in this project yet.</p>
        </div>
      ) : (
        <div className="task-list">
          {tasks.map((task) => (
            <article key={task.id} className="card task-card">
              <div>
                <span className={`priority priority-${task.priority}`}>
                  {task.priority}
                </span>
                <h3>{task.title}</h3>
                <p className="muted">{task.description}</p>
              </div>
              <div className="card-actions">
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => startEditTask(task)}
                >
                  Edit
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={() => handleDeleteTask(task.id)}
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
