class DialogSkill:
    def can_handle(self, text):
        return True  # fallback на любой нераспознанный текст

    def handle(self, user, text):
        # Очень простая имитация ответа — здесь будет интеграция с LLM/твоей моделью!
        if "привет" in text.lower():
            return "Привет! Я Саша, твой ассистент."
        return "Я пока учусь, но всегда готова поговорить!"
