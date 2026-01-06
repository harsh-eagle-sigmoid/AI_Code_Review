import type { Issue } from "../api/client";

interface BugListProps {
  issues: Issue[];
}

export default function BugList({ issues }: BugListProps) {
  if (!issues || issues.length === 0) {
    return <p style={{ marginTop: 16, color: "green" }}>No issues found 🎉</p>;
  }

  return (
    <div style={{ marginTop: 24 }}>
      {issues.map((bug, idx) => (
        <div
          key={idx}
          style={{
            padding: 12,
            borderLeft: "4px solid red",
            marginBottom: 12,
          }}
        >
          <strong>
            Line {bug.line} — {bug.severity}
          </strong>
          <p>{bug.description}</p>
          <small>Fix: {bug.suggestion}</small>
        </div>
      ))}
    </div>
  );
}
