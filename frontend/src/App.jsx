import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const checkHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) {
      setError("Please enter a query.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const healthy = await checkHealth();

      if (!healthy) {
        throw new Error(
          "Backend is not running. Start the SentinelForge backend first."
        );
      }

      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": "sentinelforge-secret-key",
        },
        body: JSON.stringify({
          query: query.trim(),
          top_k: 3,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to connect to SentinelForge.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">S</div>

          <div>
            <h1>SentinelForge</h1>
            <p>Secure RAG Intelligence</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Online
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <p className="eyebrow">RAG CONTROL CENTER</p>

          <h2>Ask SentinelForge</h2>

          <p className="hero-text">
            Search your knowledge base and receive grounded answers with
            source citations.
          </p>
        </section>

        <section className="query-card">
          <label htmlFor="query">Your question</label>

          <textarea
            id="query"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                handleQuery();
              }
            }}
            placeholder="Ask something about your knowledge base..."
            rows="4"
          />

          <div className="query-footer">
            <span>Press Enter to search</span>

            <button
              onClick={handleQuery}
              disabled={loading}
            >
              {loading ? "Searching..." : "Ask SentinelForge"}
            </button>
          </div>
        </section>

        {error && (
          <section className="error-card">
            <strong>Request failed</strong>
            <p>{error}</p>
          </section>
        )}

        {result && (
          <section className="results">
            <div className="answer-card">
              <div className="card-header">
                <div>
                  <p className="card-label">ANSWER</p>
                  <h3>Generated Response</h3>
                </div>

                <span
                  className={
                    result.grounded
                      ? "badge grounded"
                      : "badge ungrounded"
                  }
                >
                  {result.grounded ? "Grounded" : "Not Grounded"}
                </span>
              </div>

              <div className="answer">
                {result.answer || "No answer returned."}
              </div>
            </div>

            <div className="info-grid">
              <div className="info-card">
                <p className="card-label">STATUS</p>

                <div className="info-value">
                  {result.success ? "Success" : "Failed"}
                </div>

                {result.reason && (
                  <p className="muted">{result.reason}</p>
                )}
              </div>

              <div className="info-card">
                <p className="card-label">SOURCES</p>

                <div className="info-value">
                  {result.citations?.length || 0}
                </div>

                <p className="muted">Retrieved citations</p>
              </div>
            </div>

            {result.citations?.length > 0 && (
              <div className="sources-card">
                <div className="card-header">
                  <div>
                    <p className="card-label">CITATIONS</p>
                    <h3>Retrieved Sources</h3>
                  </div>
                </div>

                <div className="sources">
                  {result.citations.map((citation, index) => (
                    <div className="source" key={citation.chunk_id || index}>
                      <div className="source-number">
                        {index + 1}
                      </div>

                      <div>
                        <strong>{citation.filename}</strong>

                        <p>
                          {citation.language || "document"}
                          {citation.page
                            ? ` · Page ${citation.page}`
                            : ""}
                        </p>

                        <small>
                          Chunk: {citation.chunk_id}
                        </small>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {!result && !error && (
          <section className="empty-state">
            <div className="empty-icon">⌕</div>

            <h3>Ready for your question</h3>

            <p>
              Enter a question above to query the SentinelForge RAG
              knowledge base.
            </p>
          </section>
        )}
      </main>

      <footer>
        <span>SentinelForge</span>
        <span>Secure RAG API Dashboard</span>
      </footer>
    </div>
  );
}

export default App;

