import json

def safe_json_parse(text: str):
    """
    Safely extract and parse the first JSON object from an LLM response.
    This version is LangChain-version agnostic.
    """
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM output")

    json_str = text[start : end + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by LLM: {e}")
