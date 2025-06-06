<<<<<<< HEAD
# SASHA MVP Blueprint

Личный AI-ассистент "Саша" с локальной LLM (Llama 3 через Ollama) и Telegram-интерфейсом.

## Быстрый старт
1. Установи [Ollama](https://ollama.com/) (Windows/Mac/Linux).
2. Запусти модель:  
   `ollama run llama3`
3. Установи зависимости:  
   `pip install -r requirements.txt`
4. Вставь свой токен Telegram в configs/config.yaml.
5. Запусти:  
   `python main.py`

## Структура
- `main.py` — точка входа
- `core/agent.py` — ядро ассистента
- `core/memory.py` — база знаний/память
- `skills/qa_skill.py` — навык Q&A (LLM)
- `interfaces/telegram_bot.py` — Telegram-бот
- `configs/config.yaml` — настройки

## Как это работает?
Ассистент "Саша" подключается к Telegram, сохраняет диалоги, запрашивает ответы у локальной LLM через Ollama.
Всё хранится только у тебя — никаких внешних сервисов, максимум приватности.
=======
# sasha_ai
>>>>>>> 878700491bffaf76bf21e6ed0dd0b215c647e539
