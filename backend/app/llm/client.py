import os, json, requests

HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json",
}

def call_llm(prompt: str) -> dict:
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "temperature": 0.5},
    }
    resp = requests.post(HF_API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    text = resp.json()[0]["generated_text"]
    # parse JSON out of `text` here if you return structured output
    return {"output": text}
