import type { Issue } from "../api/client";

interface BugListProps {
  issues: Issue[];
}

export default function BugList({ issues }: BugListProps) {
  if (issues.length === 0) {
    return <p className="p-4 text-green-400">No issues found 🎉</p>;
  }

  return (
    <div className="p-4 space-y-4">
      {issues.map((bug, index) => (
        <div
          key={index}
          className="p-4 bg-gradient-to-r from-red-500/10 to-red-600/10 rounded-xl border-l-4 border-red-500"
        >
          <div className="font-bold">
            Line {bug.line} — {bug.severity}
          </div>
          <p className="text-gray-300">{bug.description}</p>
          <p className="text-gray-400 text-sm">
            Fix: {bug.suggestion}
          </p>
        </div>
      ))}
    </div>
  );
}
