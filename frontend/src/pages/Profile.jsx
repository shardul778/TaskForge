import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import Layout from "../components/Layout";

export default function Profile() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .me()
      .then((data) => setProfile(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <Layout>
      <div className="page-header">
        <h1>Profile</h1>
      </div>

      {error && <div className="alert error">{error}</div>}

      <div className="card profile-card">
        <h2>Account</h2>
        <dl className="profile-list">
          <div>
            <dt>Username</dt>
            <dd>{user}</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>{profile?.message || "—"}</dd>
          </div>
        </dl>
      </div>
    </Layout>
  );
}
