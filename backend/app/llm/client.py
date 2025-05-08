import os, json, requests
from google import genai
from google.genai import types
import re
from backend.app.core.logger import logger

gemini_api_key = os.getenv("GEMINI_API_KEY")

def call_llm(prompt: str) -> dict:
    try:
        client = genai.Client(api_key=gemini_api_key)
        logger.info(f"feeding prompt: {prompt}")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        parsed_output = extract_llm_response(response.text)
        logger.info(f"llm ouput format cleaned: {parsed_output}")
        parsed_output = parsed_output['solutions']

        return {parsed_output}

    except Exception as e:
        logger.error(f"Calling LLM failed error: {e}")


def extract_llm_response(raw_text: str) -> dict:
    """
    Extracts and parses the actual JSON object from a raw LLM string that looks like ```json\n{...}\n```
    """
    try:
        # Remove backticks and "json" marker
        cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text.strip(), flags=re.DOTALL)
        
        # Convert to dict
        parsed = json.loads(cleaned)
        return parsed
    
    except Exception as e:
        # Optional fallback
        print(f"Failed to parse LLM output: {e}")
        return {"summary": "", "diagnosis": [], "solutions": [], "confidence": 0.0}