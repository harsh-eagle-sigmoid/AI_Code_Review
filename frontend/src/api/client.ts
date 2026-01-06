import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Issue {
  file: string;
  line: number;
  severity: "LOW" | "MEDIUM" | "HIGH";
  issue_type: string;
  description: string;
  suggestion: string;
}

export interface ReviewResponse {
  issues: Issue[];
  summary: string;
}

export async function reviewCode(code: string): Promise<ReviewResponse> {
  console.log("SENDING CODE:", code);
  const res = await api.post("/review", { code });
  return res.data;
}

export default api;
