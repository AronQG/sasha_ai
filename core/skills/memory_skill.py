class MemorySkill:
    def __init__(self, memory):
        self.memory = memory

    def can_handle(self, text):
        return any(word in text.lower() for word in ["запомни", "какой", "забудь"])

    def handle(self, user, text):
        text = text.lower()
        if "запомни" in text:
            # Пример: "Саша, запомни мой любимый цвет — синий"
            key_value = text.split("запомни", 1)[1].strip()
            if "—" in key_value:
                key, value = [x.strip() for x in key_value.split("—", 1)]
            elif "-" in key_value:
                key, value = [x.strip() for x in key_value.split("-", 1)]
            else:
                return "Укажи что запомнить: 'Саша, запомни ключ — значение'"
            self.memory.set_fact(user, key, value)
            return f"Запомнила: {key} = {value}"
        elif "какой" in text:
            # Пример: "Саша, какой мой любимый цвет?"
            key = text.split("какой", 1)[1].split("?")[0].strip()
            value = self.memory.get_fact(user, key)
            return value if value else "Я не помню этого."
        elif "забудь" in text:
            key = text.split("забудь", 1)[1].strip()
            self.memory.del_fact(user, key)
            return f"Забыла {key}"
        else:
            return "Я пока не умею работать с такой памятью."
