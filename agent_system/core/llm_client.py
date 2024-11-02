import requests
from typing import Dict, Any
import json

class LLMClient:
    """Handles communication with the LLM API."""
    
    def __init__(self, api_key: str, model: str = "gpt-4-0125-preview"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def query(self, prompt: str, max_tokens: int = 150) -> str:
        """Send a query to the LLM and return the response."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            raise Exception(f"LLM query failed: {str(e)}")