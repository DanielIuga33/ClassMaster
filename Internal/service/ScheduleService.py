import json
import os


class ScheduleService:
    def __init__(self):
        self.__filename = None
        self.__schedule_data = []

    def set_schedule_path(self, new_data_path: str):
        if new_data_path:
            os.makedirs(new_data_path, exist_ok=True)
            self.__filename = os.path.join(new_data_path, "Schedule.json")
            # Dacă fișierul nu există în noua locație, îl creăm
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump({}, f)
            # Reîncărcăm lista din noua locație
            self.__schedule_data = self.load_schedule_data()

    def load_schedule_data(self):
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def get_schedule_data(self):
        return self.__schedule_data

    def save_schedule_data(self):
        os.makedirs("Data", exist_ok=True)
        with open(self.__filename, "w") as f: json.dump(self.__schedule_data, f, indent=4)
