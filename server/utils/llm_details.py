import requests

def get_shikh_details(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer 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",
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
        print(f"ERROR: {e}")
        return {
            'status': 'LLM_ERR',
            'details': '',
            'message' : {e}
        }
