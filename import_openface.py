import csv
import os
from core.memory import Memory

# Укажи здесь актуальный путь к файлу .csv от OpenFace
CSV_PATH = r"D:\OpenFace\OpenFace_2.2.0_win_x64\out\webcam_2025-06-05-18-16.csv"
USER = "local_user"

def parse_openface_csv(csv_path):
    blinks, eats, drinks, sleeps = 0, 0, 0, 0
    blink_prev = False
    sleep_closed = 0
    memory = Memory()
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Не все версии OpenFace имеют confidence, AU25_r, AU45_r — но мы пробуем максимум
            try:
                confidence = float(row.get("confidence", 1))
                if confidence < 0.90:
                    continue
                # Детект морганий — по AU45_r (blink), если доступен
                au45 = float(row.get(" AU45_r", 0) or row.get("AU45_r", 0))
                is_blink = au45 > 1.5
                if is_blink and not blink_prev:
                    blinks += 1
                    memory.log_event("blink", USER, f"blink_{blinks}", "", None)
                blink_prev = is_blink
                # Детект еды — рот широко открыт (AU25_r)
                au25 = float(row.get(" AU25_r", 0) or row.get("AU25_r", 0))
                if au25 > 2.0:
                    eats += 1
                    memory.log_event("eat", USER, f"eat_{eats}", "", None)
                # Детект питья (эвристика — AU25 чуть открыт, не сильно)
                if 1.0 < au25 < 2.0:
                    drinks += 1
                    memory.log_event("drink", USER, f"drink_{drinks}", "", None)
                # Сон — глаза закрыты > 30 кадров подряд
                if is_blink:
                    sleep_closed += 1
                    if sleep_closed > 30:
                        sleeps += 1
                        memory.log_event("sleep", USER, f"sleep_{sleeps}", "", None)
                        sleep_closed = 0
                else:
                    sleep_closed = 0
            except Exception as ex:
                continue
    print(f"Импортировано: {blinks} морганий, {eats} еды, {drinks} питья, {sleeps} сна.")

if __name__ == "__main__":
    parse_openface_csv(CSV_PATH)
