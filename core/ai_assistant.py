import httpx
import os

class SmartSasha:
    def __init__(self, memory):
        self.memory = memory
        self.llm_url = "http://127.0.0.1:1234/v1/chat/completions"  # LM Studio API

    async def chat(self, message):
        prompt = f"Ты — умный персональный ассистент. Вот вопрос пользователя:\n{message}\nОтветь максимально понятно."
        response = await self._llm_call(prompt)
        self.memory.log_event("assistant_reply", "sasha", response)
        return response

    async def generate_blender_scene(self, user_prompt):
        prompt = (
            "Ты AI-помощник для Blender. Пользователь написал: "
            f"'''{user_prompt}'''\n"
            "1. Опиши план действий для себя, как для ассистента (коротко).\n"
            "2. Затем с новой строки сгенерируй готовый python-скрипт для Blender (bpy), который создаёт соответствующую сцену. "
            "Скрипт должен включать камеру, освещение, материалы, рендер изображения в 'D:/sasha/output.png'. "
            "Сначала выведи план (в теге <plan>), потом скрипт в <code>."
        )
        llm_resp = await self._llm_call(prompt)
        plan, code = self._extract_plan_and_code(llm_resp)
        self.memory.log_event("blender_scene", "sasha", user_prompt, extra=plan)
        return plan, code

    async def _llm_call(self, prompt):
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "meta/llama-3-13b",  # или твоя модель
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1800,
            "stream": False
        }
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(self.llm_url, json=data)
            resp.raise_for_status()
            reply = resp.json()
            # Адаптируемся под структуру LM Studio/ОpenAI
            if "choices" in reply:
                return reply["choices"][0]["message"]["content"]
            return str(reply)

    def _extract_plan_and_code(self, llm_resp):
        # Очень простой парсер, можно заменить на парсинг markdown, если нужно
        import re
        plan = ""
        code = ""
        plan_match = re.search(r"<plan>(.*?)</plan>", llm_resp, re.DOTALL)
        code_match = re.search(r"<code>(.*?)</code>", llm_resp, re.DOTALL)
        if plan_match:
            plan = plan_match.group(1).strip()
        if code_match:
            code = code_match.group(1).strip()
        else:
            # если LLM выдал код без тега — пробуем вытащить его весь после первой строки
            parts = llm_resp.split("```python")
            if len(parts) > 1:
                code = parts[1].split("```")[0]
            else:
                code = llm_resp
        return plan, code
