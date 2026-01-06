REVIEW_PROMPT = """
You are a senior software engineer and security expert.

Analyze the following code diff.

Tasks:
1. Detect bugs
2. Detect security vulnerabilities
3. Suggest performance improvements
4. Assign severity: LOW, MEDIUM, HIGH, CRITICAL
5. Give a quality score (0-100)

Return STRICT JSON only.

Code Diff:
{code}
"""
