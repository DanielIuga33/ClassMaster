from Internal.repository.RepositoryStudent import RepositoryStudent


def __roman_to_int(roman):
    """Transformă cifre romane (I, V, X, XII) în numere întregi pentru sortare."""
    # Curățăm textul de caractere extra (ex: "IX-a" -> "IX")
    roman = roman.split('-')[0].upper().strip()

    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    res = 0
    for i in range(len(roman)):
        if i > 0 and roman_values[roman[i]] > roman_values[roman[i - 1]]:
            res += roman_values[roman[i]] - 2 * roman_values[roman[i - 1]]
        else:
            res += roman_values[roman[i]]
    return res


class StudentService:
    def __init__(self, repository_student: RepositoryStudent):
        self.__repository = repository_student

    def add_student(self, first_name, last_name, grade, price, teacher_id):
        """Validează datele și adaugă studentul prin repository."""
        # 1. Validări de bază
        if not first_name or not last_name or not grade:
            return [400, "Toate câmpurile sunt obligatorii!"]

        try:
            price_numeric = int(price)
            if price_numeric < 0:
                return [400, "Prețul nu poate fi negativ!"]
        except ValueError:
            return [400, "Prețul trebuie să fie un număr valid!"]

        # 2. Crearea obiectului Entity
        from Internal.entity.Student import Student
        new_student = Student(first_name.strip(), last_name.strip(), grade.strip(), price_numeric, teacher_id.strip())

        # 3. Trimiterea către repository
        return self.__repository.add_student(new_student)

    def get_all_students(self):
        """Returnează lista completă de studenți."""
        return self.__repository.get_all()

    def get_student_by_id(self, id_stud):
        return self.__repository.get_stud_by_id(id_stud)

    def remove_student(self, student):
        return self.__repository.remove_student(student)

    def modify_student(self, student_old, student_new):
        return self.__repository.modify_student(student_old, student_new)

    def get_students_for_teacher(self, id_teacher: str):
        result = []
        for student in self.get_all_students():
            if student.get_teacher_id() == id_teacher:
                result.append(student)
        return result

    def get_sorted_students(self, id_teacher: str, criteria="grade"):
        """Returnează lista de studenți sortată conform criteriului, inclusiv cifre romane."""
        students = self.get_students_for_teacher(id_teacher)

        if criteria == "grade":
            # Folosim funcția de conversie pentru a sorta numeric clasele
            try:
                return sorted(students, key=lambda s: __roman_to_int(s.get_grade()))
            except:
                # Fallback în caz că formatul clasei nu este cifră romană validă
                return sorted(students, key=lambda s: s.get_grade())

        elif criteria == "price":
            return sorted(students, key=lambda s: s.get_price(), reverse=True)
        elif criteria == "name":
            return sorted(students, key=lambda s: (s.get_last_name(), s.get_first_name()))

        return students

    # Delegăm restul operațiilor către repository
    # def add_student(self, first_name, last_name, grade, price):
    #     from Internal.entity.Student import Student
    #     new_student = Student(first_name, last_name, grade, int(price))
    #     return self.__repository.add_student(new_student)

    def delete_student(self, student):
        return self.__repository.remove_student(student)

    def set_repository_path(self, path):
        self.__repository.set_new_path(path)

