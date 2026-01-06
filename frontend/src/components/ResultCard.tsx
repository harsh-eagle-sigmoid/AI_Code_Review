import type { Issue } from "../api/client";

interface ResultCardProps {
  summary: string;
  issues: Issue[];
}

export default function ResultCard({ summary, issues }: ResultCardProps) {
  const score = Math.max(0, 100 - issues.length * 10);

  return (
    <div style={{ marginTop: 24, padding: 16, border: "1px solid #444" }}>
      <h3>Review Summary</h3>
      <p>{summary}</p>

      <div style={{ marginTop: 12 }}>
        <strong>Quality Score:</strong> {score}
      </div>
      <div>
        <strong>Issues Found:</strong> {issues.length}
      </div>
    </div>
  );
}
