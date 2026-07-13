import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-left">
          <Link to="/dashboard" className="brand">
            ⚒ TaskForge
          </Link>
          <nav className="nav">
            <Link
              to="/dashboard"
              className={location.pathname === "/dashboard" ? "active" : ""}
            >
              Projects
            </Link>
            <Link
              to="/profile"
              className={location.pathname === "/profile" ? "active" : ""}
            >
              Profile
            </Link>
          </nav>
        </div>
        <div className="topbar-right">
          <span className="welcome">Hello, {user}</span>
          <button type="button" className="btn btn-ghost" onClick={logout}>
            Logout
          </button>
        </div>
      </header>
      <main className="main-content">{children}</main>
    </div>
  );
}
