import csv
import datetime

# Маппинг колонок под твой CSV. Настрой если будут отличия!
COLUMNS = {
    "blink": " AU45_r",  # Ищем моргания по AU45_r (Action Unit 45 - Blink)
    "eat": None,         # Пока нет, можно сделать по ключевому слову или другой AU
    "drink": None,       # Аналогично
    "smile": " AU12_r",  # Улыбка по AU12_r
    # ...добавь по необходимости
}

THRESHOLDS = {
    "blink": 2.0,    # Подбери по своей камере, это пример
    "smile": 2.0,    # Пример
    # ...
}

class OpenFaceImporter:
    def __init__(self, memory):
        self.memory = memory

    def import_from_csv(self, path):
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            last_blink = False
            last_smile = False
            blink_count = 0
            smile_count = 0
            for row in reader:
                ts = self._row_timestamp(row)
                # Моргание
                blink_val = float(row.get(" AU45_r", "0"))
                if blink_val > THRESHOLDS["blink"] and not last_blink:
                    self.memory.log_event("blink", "local_user", "1", timestamp=ts)
                    blink_count += 1
                    last_blink = True
                elif blink_val <= THRESHOLDS["blink"]:
                    last_blink = False
                # Улыбка
                smile_val = float(row.get(" AU12_r", "0"))
                if smile_val > THRESHOLDS["smile"] and not last_smile:
                    self.memory.log_event("smile", "local_user", "1", timestamp=ts)
                    smile_count += 1
                    last_smile = True
                elif smile_val <= THRESHOLDS["smile"]:
                    last_smile = False
            print(f"Импортировано: {blink_count} морганий, {smile_count} улыбок.")
    
    def _row_timestamp(self, row):
        # OpenFace обычно пишет timestamp или frame timestamp
        if " timestamp" in row:
            # в секундах, прибавляем к сегодняшнему дню
            seconds = float(row[" timestamp"])
            base = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            ts = base + datetime.timedelta(seconds=seconds)
            return ts.isoformat()
        else:
            return datetime.datetime.now().isoformat()
