import os
import threading
import time
from core.memory import Memory
from core.skills.report_skill import ReportSkill
from core.openface_importer import OpenFaceImporter
from interfaces.telegram_bot import run_telegram_bot

OPENFACE_OUT = r"D:/OpenFace/OpenFace_2.2.0_win_x64/out"
CSV_PATTERN = "webcam_*.csv"

def openface_watcher(memory):
    """Отслеживает новые CSV и импортирует события."""
    importer = OpenFaceImporter(memory)
    processed = set()
    while True:
        files = [f for f in os.listdir(OPENFACE_OUT) if f.endswith('.csv')]
        for fname in files:
            full_path = os.path.join(OPENFACE_OUT, fname)
            if full_path not in processed:
                print(f"Импортирую {full_path}")
                try:
                    importer.import_from_csv(full_path)
                    processed.add(full_path)
                except Exception as e:
                    print(f"Ошибка импорта {fname}: {e}")
        time.sleep(5)  # Проверять раз в 5 сек

def main():
    memory = Memory()
    # Запускаем watcher для OpenFace в отдельном потоке
    threading.Thread(target=openface_watcher, args=(memory,), daemon=True).start()
    report = ReportSkill(memory)
    run_telegram_bot(memory, report)

if __name__ == "__main__":
    main()
