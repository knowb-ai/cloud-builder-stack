import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  const [health, setHealth] = useState("checking");

  useEffect(() => {
    fetch("/api/health")
      .then((response) => response.json())
      .then((data) => setHealth(data.status ?? "unknown"))
      .catch(() => setHealth("unreachable"));
  }, []);

  return (
    <main className="app-shell">
      <section className="intro">
        <p className="eyebrow">Cloud Builder Stack</p>
        <h1>FastAPI backend, bundled frontend, ready to deploy.</h1>
        <p>
          Start small, keep secrets server-side, and ship the SPA through the
          backend when a single-service deploy is the fastest path.
        </p>
      </section>

      <section className="status-panel" aria-label="Backend status">
        <span>Backend</span>
        <strong>{health}</strong>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
