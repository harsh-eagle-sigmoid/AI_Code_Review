import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Issue {
  line: number;
  severity: "LOW" | "MEDIUM" | "HIGH";
  description: string;
  suggestion: string;
  issue_type: string;
}

export interface ReviewResponse {
  summary: string;
  bugs: Issue[];
}

export async function reviewCode(code: string): Promise<ReviewResponse> {
  console.log("SENDING CODE:", code);
  console.log("API URL:", import.meta.env.VITE_API_URL);

  const res = await api.post("/review", { code });

  const bugs = Array.isArray(res.data?.bugs)
    ? res.data.bugs.map((bug: any) => ({
        line: typeof bug.line === "number" ? bug.line : 0,
        severity: bug.severity ?? "LOW",
        description: bug.description ?? "No description provided",
        suggestion: bug.suggestion ?? "No suggestion provided",
        issue_type: bug.issue_type ?? "General",
      }))
    : [];

  console.log("NORMALIZED BUGS:", bugs);

  return {
    summary: res.data?.summary ?? "Review completed",
    bugs,
  };
}

export default api;
