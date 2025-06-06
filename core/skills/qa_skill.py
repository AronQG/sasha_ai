import requests

class QASkill:
    def __init__(self, llm_url, llm_model):
        self.llm_url = llm_url
        self.llm_model = llm_model

    def can_handle(self, text):
        return True  # обработка всех вопросов

    def handle(self, user, text):
        # Можно добавить историю (если хочешь диалоговость)
        messages = [
            {"role": "system", "content": "Ты Саша — личный AI-ассистент, говори по-русски, отвечай дружелюбно и понятно."},
            {"role": "user", "content": text},
        ]
        data = {
            "model": self.llm_model,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7,
        }
        try:
            resp = requests.post(self.llm_url, json=data, timeout=60)
            resp.raise_for_status()
            response = resp.json()
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Ошибка LLM: {e}"
