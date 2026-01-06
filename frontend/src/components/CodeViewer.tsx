import type { Issue } from "../api/client";

interface CodeViewerProps {
  code: string;
  issues: Issue[];
}

export default function CodeViewer({ code, issues }: CodeViewerProps) {
  const issueMap = new Map<number, Issue["severity"]>(
    issues.map((i) => [i.line, i.severity])
  );

  return (
    <div className="card code-viewer">
      {code.split("\n").map((line, index) => {
        const lineNo = index + 1;
        const severity = issueMap.get(lineNo);

        const severityClass =
          severity === "HIGH"
            ? "high"
            : severity === "MEDIUM"
            ? "medium"
            : "";

        return (
          <div key={index} className={`code-line ${severityClass}`}>
            <span className="line-num">{lineNo}</span>
            <span>{line}</span>
          </div>
        );
      })}
    </div>
  );
}
