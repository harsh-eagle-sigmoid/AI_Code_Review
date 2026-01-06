import type { Issue } from "../api/client";

interface ResultCardProps {
  summary: string;
  issues: Issue[];
}

export default function ResultCard({ summary, issues = [] }: ResultCardProps) {
  const score = Math.max(0, 100 - issues.length * 10);

  return (
    <div className="mt-6 bg-gray-900 rounded-xl p-6">
      <h3 className="text-xl font-bold mb-2">Review Summary</h3>

      <p className="mb-4">{summary}</p>

      <div className="flex gap-6">
        <div>
          <div className="text-3xl font-bold text-green-400">{score}</div>
          <div className="text-sm">Quality Score</div>
        </div>

        <div>
          <div className="text-3xl font-bold text-red-400">
            {issues.length}
          </div>
          <div className="text-sm">Issues Found</div>
        </div>
      </div>
    </div>
  );
}
