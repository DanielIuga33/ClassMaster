from Internal.repository.RepositoryStudent import RepositoryStudent


def __roman_to_int(roman):
    """Transformă cifre romane (I, V, X, XII) în numere întregi pentru sortare."""
    if not roman: return 0
    # Curățăm textul de caractere extra (ex: "IX-a" -> "IX")
    roman = str(roman).split('-')[0].upper().strip()

    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    res = 0
    try:
        for i in range(len(roman)):
            if i > 0 and roman_values[roman[i]] > roman_values[roman[i - 1]]:
                res += roman_values[roman[i]] - 2 * roman_values[roman[i - 1]]
            else:
                res += roman_values[roman[i]]
        return res
    except KeyError:
        return 0


class StudentService:
    def __init__(self, repository_student: RepositoryStudent):
        self.__repository = repository_student
        # Atribute pentru starea toggle-ului de sortare
        self.__last_criteria = None
        self.__reverse_toggle = False

    def add_student(self, first_name, last_name, grade, price, teacher_id):
        """Validează datele și adaugă studentul prin repository."""
        if not grade:
            return [400, "Toate câmpurile sunt obligatorii!"]

        try:
            price_numeric = int(price)
            if price_numeric < 0:
                return [400, "Prețul nu poate fi negativ!"]
        except ValueError:
            return [400, "Prețul trebuie să fie un număr valid!"]

        from Internal.entity.Student import Student
        new_student = Student(first_name.strip(), last_name.strip(), grade.strip(), price_numeric, teacher_id.strip())
        return self.__repository.add_student(new_student)

    def get_all_students(self):
        return self.__repository.get_all()

    def get_student_by_id(self, id_stud):
        return self.__repository.get_stud_by_id(id_stud)

    def get_students_by_id_list(self, id_list):
        result = []
        for id_stud in id_list:
            student = self.get_student_by_id(id_stud)
            if student:
                result.append(student)
        return result

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
        """Returnează lista sortată conform criteriului, cu funcție de toggle."""
        students = self.get_students_for_teacher(id_teacher)

        # Logică Toggle: Dacă se apasă același criteriu, inversăm ordinea
        if criteria == self.__last_criteria:
            self.__reverse_toggle = not self.__reverse_toggle
        else:
            self.__last_criteria = criteria
            self.__reverse_toggle = False

        if criteria == "grade":
            try:
                # Sortare numerică folosind conversia din cifre romane
                students.sort(key=lambda s: __roman_to_int(s.get_grade()), reverse=self.__reverse_toggle)
            except:
                students.sort(key=lambda s: str(s.get_grade()), reverse=self.__reverse_toggle)

        elif criteria == "price":
            # Sortare după preț
            students.sort(key=lambda s: int(s.get_price()), reverse=self.__reverse_toggle)

        elif criteria == "name":
            # Sortare alfabetică (Nume, apoi Prenume) ignorând diferențele de litere mari/mici
            students.sort(key=lambda s: (s.get_last_name().lower(), s.get_first_name().lower()),
                          reverse=self.__reverse_toggle)

        return students

    def delete_student(self, student):
        return self.__repository.remove_student(student)

    def set_repository_path(self, path):
        self.__repository.set_new_path(path)
