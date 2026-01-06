import { Bug, Zap, Play, CheckCircle, Loader2 } from "lucide-react";
import { useEffect, useState } from "react";

import StarBackground from "../components/StarBackground";
import StatsPanel from "../components/StatsPanel";

import { reviewCode } from "../api/client";
import type { Issue } from "../api/client";

export default function ReviewDetails() {
  const [code, setCode] = useState("x = 1\nprint(x)");
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(false);
  const [executionTime, setExecutionTime] = useState(0);
  const [status, setStatus] = useState<"idle" | "running" | "done">("idle");

  const runReview = async () => {
    setLoading(true);
    setStatus("running");
    const start = Date.now();

    const res = await reviewCode(code);

    setIssues(res.issues);
    setExecutionTime(Date.now() - start);
    setLoading(false);
    setStatus("done");
  };

  // Keyboard shortcut: Ctrl/Cmd + Enter
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        runReview();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [code]);

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white">
      <StarBackground />

      <div className="relative z-10 max-w-7xl mx-auto p-6 space-y-8">

        {/* HEADER */}
        <div className="bg-black/40 backdrop-blur-xl rounded-2xl border border-white/10 p-6 shadow-2xl
                        glow-card glow-hover glow-cyan">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                Code Debugger Pro
              </h1>
              <p className="text-gray-300 mt-1">
                AI-powered static analysis & security review
              </p>
            </div>

            <div className="flex items-center gap-4">
              {/* STATUS */}
              {status === "running" && (
                <span className="flex items-center gap-2 text-yellow-400">
                  <Loader2 className="animate-spin w-4 h-4" />
                  Analyzing
                </span>
              )}
              {status === "done" && (
                <span className="flex items-center gap-2 text-green-400">
                  <CheckCircle className="w-4 h-4" />
                  Complete
                </span>
              )}

              <div className="flex items-center gap-2 bg-black/30 px-4 py-2 rounded-xl">
                <Zap className="text-yellow-400 w-5 h-5" />
                <span className="text-sm">{executionTime}ms</span>
              </div>
            </div>
          </div>
        </div>

        {/* MAIN GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

          {/* CODE PANEL (PRIMARY) */}
          <div className="lg:col-span-2 bg-gray-900/90 rounded-2xl border border-gray-700 shadow-2xl
                          glow-card glow-hover glow-cyan">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-96 bg-gray-900 text-gray-100 font-mono p-6 outline-none resize-none"
              placeholder="Paste your code here..."
            />

            <div className="p-4">
              <button
                onClick={runReview}
                disabled={loading}
                className="flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-500
                           px-6 py-2 rounded-xl font-semibold shadow-lg
                           hover:scale-[1.03] transition disabled:opacity-50"
              >
                <Play size={16} />
                {loading ? "Analyzing..." : "Run Review"}
              </button>
              <p className="text-xs text-gray-400 mt-2">
                Press Ctrl / Cmd + Enter
              </p>
            </div>
          </div>

          {/* DEBUG PANEL (SECONDARY) */}
          <div className="bg-gray-900/70 rounded-2xl border border-gray-700 shadow-2xl
                          glow-card glow-hover glow-red">
            <div className="p-4 border-b border-gray-700 flex items-center gap-2">
              <Bug className="text-red-400" />
              <h2 className="font-bold">Debug Panel</h2>
            </div>

            <div className="p-4 space-y-3">
              {issues.length === 0 && (
                <p className="text-sm text-gray-400">
                  No issues yet. Run a review.
                </p>
              )}

              {issues.map((issue, i) => (
                <div
                  key={i}
                  className={`p-3 rounded-xl border-l-4
                    ${issue.severity === "HIGH"
                      ? "bg-red-500/10 border-red-500"
                      : issue.severity === "MEDIUM"
                      ? "bg-yellow-500/10 border-yellow-500"
                      : "bg-green-500/10 border-green-500"
                    }`}
                >
                  <strong>Line {issue.line}</strong>
                  <p className="text-sm text-gray-300 mt-1">
                    {issue.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* STATS PANEL (TERTIARY) */}
        <StatsPanel issues={issues} code={code} />

      </div>
    </div>
  );
}
