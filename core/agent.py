from core.skills.memory_skill import MemorySkill
from core.skills.qa_skill import QASkill  # <--- вот он!
# from core.skills.dialog_skill import DialogSkill  # больше не нужен

class SashaAgent:
    def __init__(self, memory, llm_url="http://127.0.0.1:1234/v1/chat/completions", llm_model="llama-3-13b-instruct"):
        self.skills = [
            MemorySkill(memory),
            QASkill(llm_url, llm_model),  # <-- вот он!
            # DialogSkill()  # fallback больше не нужен!
        ]

    def handle_message(self, user, text):
        for skill in self.skills:
            if skill.can_handle(text):
                return skill.handle(user, text)
        return "Я не знаю, как на это ответить."
