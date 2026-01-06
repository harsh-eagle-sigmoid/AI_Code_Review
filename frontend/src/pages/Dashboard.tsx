import { useState } from "react";
import api from "../api/client";
import BugList from "../components/BugList";
import ResultCard from "../components/ResultCard";
import type { Issue } from "../api/client";

interface ReviewResult {
  summary: string;
  bugs: Issue[];
}

export default function Dashboard() {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runReview = async () => {
    if (!code.trim()) {
      setError("Please paste some code first");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await api.post("/review", { code });

      // 🔒 HARD NORMALIZATION
      setResult({
        summary: res.data?.summary ?? "No summary returned",
        bugs: Array.isArray(res.data?.bugs) ? res.data.bugs : [],
      });
    } catch (e) {
      setError("AI review failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "auto" }}>
      <h1>AI Code Review Platform</h1>

      <textarea
        rows={12}
        style={{ width: "100%", marginTop: 16 }}
        placeholder="Paste your code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <button
        style={{ marginTop: 12 }}
        onClick={runReview}
        disabled={loading}
      >
        {loading ? "Reviewing..." : "Run AI Review"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* ✅ SAFE RENDER */}
      {result && (
        <>
          <ResultCard summary={result.summary} issues={result.bugs} />
          <BugList issues={result.bugs} />
        </>
      )}
    </div>
  );
}
