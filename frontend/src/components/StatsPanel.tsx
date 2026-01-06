import { useEffect, useState } from "react";
import type { Issue } from "../api/client";

interface Props {
  issues: Issue[];
  code: string;
}

export default function StatsPanel({ issues, code }: Props) {
  const totalLines = code.split("\n").length;
  const critical = issues.filter(i => i.severity === "HIGH").length;
  const warnings = issues.filter(i => i.severity === "MEDIUM").length;
  const clean = Math.max(totalLines - issues.length, 0);

  const useCount = (value: number) => {
    const [count, setCount] = useState(0);
    useEffect(() => {
      let current = 0;
      const step = Math.max(1, Math.ceil(value / 20));
      const interval = setInterval(() => {
        current += step;
        if (current >= value) {
          setCount(value);
          clearInterval(interval);
        } else {
          setCount(current);
        }
      }, 20);
      return () => clearInterval(interval);
    }, [value]);
    return count;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Stat title="Critical Errors" value={useCount(critical)} color="red" />
      <Stat title="Warnings" value={useCount(warnings)} color="yellow" />
      <Stat title="Clean Lines" value={useCount(clean)} color="green" />
    </div>
  );
}

function Stat({ title, value, color }: any) {
  return (
    <div className={`rounded-2xl p-6 border bg-${color}-500/10 border-${color}-500/20
                     glow-card glow-hover glow-${color}`}>
      <div className={`text-3xl font-bold text-${color}-400`}>{value}</div>
      <div className="text-gray-300 mt-1">{title}</div>
    </div>
  );
}
