import requests
import os

API_KEY = os.getenv('openrouter_api_key_ahmed_ragab_ai')
def get_shikh_details(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Shikh Classification App"
        }

        payload = {
            "model": "moonshotai/kimi-k2:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        }


        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        # Receiving request from JS
        return {
            'status': 'SUCCESS',
            'details': content
        }

    except Exception as e:
        # For Debugging
        print(f"ERROR: {e}")
        return {
            'status': 'LLM_ERR',
            'details': '',
            'message' : {e}
        }
