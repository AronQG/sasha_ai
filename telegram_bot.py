import os
import openai
import subprocess
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# --- ТВОИ НАСТРОЙКИ ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"  # путь к Blender
OUTPUT_IMAGE = r"D:\sasha\output.png"  # итоговый рендер
SCRIPT_PATH = r"D:\sasha\blender_job.py"  # скрипт для Blender

# --- Генерация Blender-кода через GPT-4 ---
def generate_blender_script(prompt):
    system_prompt = (
        "Ты профессиональный ассистент Blender 4.4. "
        "Ты отвечаешь только валидным Python-кодом, без комментариев и текста. "
        "Код должен генерировать сцену Blender по запросу пользователя. "
        "Финальный рендер сцены должен сохраняться в путь D:/sasha/output.png."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        api_key=OPENAI_API_KEY,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=2048,
    )
    # Извлекаем только чистый код (без комментариев и пояснений)
    code = response['choices'][0]['message']['content']
    # Если GPT обернул код в ```python ... ``` — убираем обертку
    if code.startswith("```"):
        code = code.split("```")[1]
        code = code.replace("python", "", 1).strip()
    return code

# --- Запуск Blender с внешним скриптом ---
def run_blender_script(script_path):
    # Для путей с пробелами обязательно в кавычки!
    command = [BLENDER_PATH, "--background", "--python", script_path]
    subprocess.run(command, check=True)

# --- Telegram-обработчик ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Генерирую сцену в Blender через GPT-4, ожидайте…")
    # Получаем скрипт для Blender от GPT-4
    code = generate_blender_script(user_text)
    # Сохраняем скрипт в файл
    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        # Удаляем старый рендер если есть (чтобы не было пересылки старого)
        if os.path.exists(OUTPUT_IMAGE):
            os.remove(OUTPUT_IMAGE)
        run_blender_script(SCRIPT_PATH)
        # Проверяем что картинка создана и отправляем ее
        if os.path.exists(OUTPUT_IMAGE):
            await update.message.reply_photo(InputFile(OUTPUT_IMAGE), caption="Вот результат работы в Blender!")
        else:
            await update.message.reply_text("Blender не смог сохранить картинку. Проверь путь и права.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации Blender-сцены: {e}")

# --- Основной запуск Telegram-бота ---
if __name__ == "__main__":
    TELEGRAM_TOKEN = "7799954702:AAG6q1c72xXof9QYMUVPBlcgxlKPR1KngCU"  # Вставь свой токен сюда!
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Бот запущен!")
    app.run_polling()
