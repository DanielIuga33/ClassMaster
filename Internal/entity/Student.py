from Internal.entity.Entity import Entity


class Student(Entity):
    def __init__(self, first_name: str, last_name: str, grade: str, price: int):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade
        self.price = price

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_grade(self):
        return self.grade

    def get_price(self):
        return self.price
