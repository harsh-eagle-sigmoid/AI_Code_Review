import { useState } from "react";
import { api } from "../api/client";
import BugList from "../components/BugList";
import ResultCard from "../components/ResultCard";

export default function Dashboard() {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runReview = async () => {
    if (!code.trim()) {
      setError("Please paste some code first");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await api.post("/review", {
        diff: code,
      });

      setResult(response.data.review);
    } catch (err) {
      setError("AI review failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "24px", maxWidth: "900px", margin: "auto" }}>
      <h1>AI Code Review Platform</h1>

      {/* CODE INPUT */}
      <textarea
        rows={12}
        style={{ width: "100%", marginTop: "16px" }}
        placeholder="Paste your code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <br />

      <button
        style={{ marginTop: "12px" }}
        onClick={runReview}
        disabled={loading}
      >
        {loading ? "Reviewing..." : "Run AI Review"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <>
          <ResultCard score={result.score} />
          <BugList bugs={result.bugs} />
        </>
      )}
    </div>
  );
}
