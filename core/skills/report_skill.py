import datetime

class ReportSkill:
    def __init__(self, memory):
        self.memory = memory

    def get_daily_report(self, user="local_user"):
        today = datetime.date.today().isoformat()
        events = self.memory.get_events(user=user, start_time=f"{today}T00:00:00", end_time=f"{today}T23:59:59")
        counts = dict(
            blink=0,
            smile=0,
            eat=0,
            drink=0,
            sleep=0,
            snapshot=0
        )
        for event in events:
            etype = event[1]
            if etype in counts:
                counts[etype] += 1
        report = (
            f"\U0001F4CA Отчёт за {today}:\n"
            f"Морганий: {counts['blink']}\n"
            f"Улыбок: {counts['smile']} 😄\n"
            f"Приёмов пищи: {counts['eat']} \U0001F374\n"
            f"Питие: {counts['drink']} \U0001F964\n"
            f"Сон: {counts['sleep']} \U0001F634\n"
            f"Снимков: {counts['snapshot']} \U0001F4F7"
        )
        return report
