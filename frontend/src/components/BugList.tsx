import type { Issue } from "../api/client";

type BugListProps = {
  issues: Issue[];
};

const BugList = ({ issues }: BugListProps) => {
  if (!issues || issues.length === 0) {
    return <p className="p-4 text-green-400">No issues found 🎉</p>;
  }

  return (
    <div className="p-4 space-y-4">
      {issues.map((bug, index) => (
        <div
          key={index}
          className="p-4 bg-red-500/10 rounded-xl border-l-4 border-red-500"
        >
          <div className="font-bold">
            Line {bug.line} — {bug.severity}
          </div>
          <p>{bug.description}</p>
          <p className="text-sm opacity-70">
            Fix: {bug.suggestion}
          </p>
        </div>
      ))}
    </div>
  );
};

export default BugList;
