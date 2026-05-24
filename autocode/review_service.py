# pyrefly: ignore [missing-import]
import json
import re
from typing import Dict, Any
# pyrefly: ignore [missing-import]
from groq import Groq
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os
import config

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """You are an expert senior code reviewer, software architect, and security engineer.
Your task is to analyze the provided code and generate a comprehensive, highly accurate review in JSON format.

Your review must evaluate the code along these 5 dimensions:
1. Bugs & Logical Errors: Check for edge cases, null pointer exceptions, unhandled runtime errors, incorrect logic, syntax errors, and infinite loops.
2. Security Vulnerabilities: Scan for injection risks (SQLi, Command, XSS), insecure data handling, hardcoded secrets, weak cryptographic practices, and buffer overflows.
3. Performance Bottlenecks: Detect inefficient algorithms, redundant operations, resource leaks (file handles, database connections), unnecessary memory allocations, and blocking synchronous calls.
4. Readability & Style: Check for unclear naming conventions, excessive nesting, missing comments, overly complex functions, and violations of standard code formatting guidelines.
5. Best Practices: Evaluate alignment with idiomatic patterns, proper error handling/logging, modern language-specific features, and code reusability.

You MUST respond strictly with a single JSON object. Do not output any markdown formatting, preambles, or postambles outside the JSON block.

The JSON response MUST exactly conform to the following schema:
{
  "summary": {
    "score": <int: 0 to 100 reflecting code health, where 100 is pristine and 0 has critical safety flaws>,
    "overview": "<string: A high-level qualitative assessment summarizing the main findings of the code review>"
  },
  "issues": [
    {
      "category": "<string: Must be one of: Bugs & Logical Errors, Security Vulnerabilities, Performance Bottlenecks, Readability & Style, Best Practices>",
      "severity": "<string: Must be one of: Critical, Warning, Optimization, Info>",
      "line_number": <int or null: The 1-based line number where the issue begins, or null if it applies globally>,
      "description": "<string: Precise description of the issue, explaining why it is a problem>",
      "suggested_fix": "<string: Concrete explanation of how to resolve the issue>"
    }
  ],
  "improved_code": "<string: The complete, fully refactored, and improved code containing all fixes and enhancements. Maintain correct syntax and indentation. Escape tabs and newlines correctly inside this JSON string.>"
}
"""

def clean_and_parse_json(response_text: str) -> Dict[str, Any]:
    """
    Cleans raw model response of potential markdown wrapping and parses it as JSON.
    """
    cleaned = response_text.strip()
    
    # Remove markdown code blocks if present
    if cleaned.startswith("```"):
        match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
            
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        json_match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        raise e

def review_code(code: str, language: str = "Python", api_key: str = None) -> Dict[str, Any]:
    """
    Calls the Groq API to review the code and returns the parsed result.
    """
    # Resolve API Key dynamically: passed argument > environment variable
    resolved_api_key = api_key or os.getenv("GROQ_API_KEY")
    
    if not resolved_api_key:
        return {
            "success": False,
            "error": "Groq API key is missing. Please provide a valid key in the sidebar or env variables."
        }
        
    if not code.strip():
        return {
            "success": False,
            "error": "No code provided for review."
        }

    try:
        # Initialize Groq client dynamically inside function
        client = Groq(api_key=resolved_api_key)
        
        user_content = f"Language: {language}\n\nCode to review:\n```\n{code}\n```"
        
        # Use active model from config (llama-3.3-70b-versatile)
        model_name = getattr(config, "GROQ_MODEL", "llama-3.3-70b-versatile")
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            model=model_name,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        parsed_data = clean_and_parse_json(response_text)
        
        # Basic schema validation
        if "summary" not in parsed_data:
            parsed_data["summary"] = {"score": 70, "overview": "Code reviewed successfully, but summary was structured incorrectly."}
        if "issues" not in parsed_data or not isinstance(parsed_data["issues"], list):
            parsed_data["issues"] = []
        if "improved_code" not in parsed_data:
            parsed_data["improved_code"] = code
            
        return {
            "success": True,
            "data": parsed_data
        }
        
    except json.JSONDecodeError as jde:
        return {
            "success": False,
            "error": f"Failed to parse AI response. The model output was not valid JSON. Detail: {str(jde)}",
            "raw_response": response_text if 'response_text' in locals() else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred during API communication: {str(e)}"
        }