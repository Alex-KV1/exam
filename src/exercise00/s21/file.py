Golden_Ratio = 1.6180339887
from random import randint, choices, random, choice


class File:
    _isistenc = None

    def __new__(cls, *args):
        if not cls._isistenc:
            cls._isistenc = super(File, cls).__new__(cls)
        return cls._isistenc

    def __init__(self, file_name: str = None) -> None:
        self.file_name = file_name

    def __call__(self, file_name):
        self.file_name = file_name
        self.openfile(self.file_name)

    def openfile(self, file_name=None) -> list:
        if file_name:
            self.file_name = file_name
        if self.file_name is not None:
            try:
                with open(self.file_name, "r", encoding="utf-8") as file:
                    return [i.rstrip("\n") for i in file.readlines()]
            except Exception as e:
                print(f"ОШИБКА: {e}")
        else:
            print(
                "ОШИБКА: Необходимо ввести путь до файла и имя файла чтобы его открыть"
            )


class Qestions:
    def __init__(self, file_name: str = "questions.txt") -> None:
        self.qusetions = File(file_name).openfile()
        self.dc_questions = dict()

    def pull_ticket(self) -> str:
        pulled_ticket = randint(0, len(self.qusetions) - 1)
        return self.qusetions[pulled_ticket]

    def take_list_questions(self) -> list:
        return self.qusetions

    def best_questions(self, len_stud):
        answer = ""
        for key in self.dc_questions:
            if self.dc_questions[key] > abs(len_stud - len(self.qusetions)):
                answer = answer + f", {key}" if answer else key
        return answer


class Examinator:
    def __init__(self, name, gender) -> None:
        self._name = name
        self._gender = gender
        self.compatibility = (self._name, self._gender)
        self.student_conut = []
        self.failed_student = []
        self.curent_student = "-"
        self.time = 0
        self.time_for_braek = 0
        self.zavalil = 0

    @property
    def st_filed(self) -> int:
        return len(self.failed_student)

    @property
    def name(self) -> str:
        return self._name

    @property
    def compat(self) -> tuple:
        return self.compatibility

    @property
    def student_ct(self) -> int:
        return len(self.student_conut)

    @student_ct.setter
    def student_ct(self, student) -> None:
        self.student_conut.append(student)


class Examinators:
    def __init__(self, file_name: str = "examiners.txt") -> None:
        self.examinators = [
            Examinator(i.split()[0], i.split()[1]) for i in File(file_name).openfile()
        ]
        # self.examinators = [{i.split()[0] :Examinator(i.split()[0], i.split()[1])} for i in File(file_name).openfile()]

    def give_teacher(self) -> str:
        index = randint(0, len(self.examinators) - 1)
        return self.examinators[index]

    @staticmethod
    def probability_choos(qustion: str, teacher: Examinator):
        '''teacher_name - строка по типу "Дарья"'''
        q = qustion
        probability = []
        for i in range(len(q)):
            tp = 1
            for j in range(0, i):
                tp = tp - probability[j]
            probability.append(tp / Golden_Ratio)
        if teacher._gender.lower() == "ж":
            probability.reverse()
        return probability

    @staticmethod
    def teacher_choos(q: str, teacher: Examinator) -> list:
        chosen_answers = set()
        q = q.split()
        probability = Examinators.probability_choos(q, teacher)
        first_choice = choices(q, weights=probability, k=1)[0]
        chosen_answers.add(first_choice)
        while True:
            if random() < (1 / 3):  # Вероятность 1/3
                new_choice = choices(q, weights=probability, k=1)[0]
                chosen_answers.add(new_choice)
            else:
                break
        return list(chosen_answers)

    def print(self):
        for i in self.examinators:
            print(i._name, i._gender, i.compatibility)


class Student:
    def __init__(self, name, gender) -> None:
        self._name = name
        self._gender = gender
        self.bal = 0
        self.resault = "Очередь"
        self.examinator = None
        self.exam_time = 0

    @property
    def name(self) -> tuple[str, str]:
        """Возвращает кортеж фамилия имя"""
        return (self._name, self._gender)

    @name.setter
    def name(self, person: tuple[str, str]):
        """Устанавливает (изменяет) Фамилию, Имя"""
        if not isinstance(person[0], str) or not isinstance(person[1], str):
            raise ValueError("Фамилия и имя должны быть строками")
        self._name = person[0]
        self._gender = person[1]

    @property
    def get_gender(self) -> str:
        return self._gender.lower()

    @property
    def get_name(self) -> str:
        return self._name

    @property
    def get_resault(self) -> str:
        return self.resault

    def probability_choos(self, qustion: str):
        q = qustion.split()
        probability = []
        for i in range(len(q)):
            tp = 1
            for j in range(0, i):
                tp = tp - probability[j]
            probability.append(tp / Golden_Ratio)
        if self.get_gender == "ж":
            probability.reverse()
        return probability

    def i_choos(self, qustion: str):
        probability = self.probability_choos(qustion)
        return choices(qustion.split(), weights=probability, k=1)[0]


class Students(File):
    def __new__(cls, args=None):
        if not hasattr(cls, "_obj"):
            cls._obj = super(Students, cls).__new__(cls)
        return cls._obj

    def __init__(self, file_name="students.txt") -> None:
        self.data: dict[str, Student] = dict()
        self.init(file_name)

    def init(self, file_name="students.txt") -> None:
        file = self.openfile(file_name)  ##!!!!
        temp = [tuple(i.split()) for i in file]
        for last_gender, name in temp:
            self.data[last_gender] = Student(last_gender, name)

    def make_quee(self):
        self.quee = []
        for item in self.data:
            self.quee.append((self.data[item].get_name, self.data[item].get_gender))

    def quee_student(self) -> tuple:
        if not hasattr(self, "quee"):
            self.make_quee()
        return self.quee.pop(0) if len(self.quee) > 0 else None

    def print(self) -> None:
        for item in self.data:
            print(f"имя {self.data[item].get_name}, Пол: {self.data[item].get_gender}")


class View:
    _isistenc = None

    def __new__(cls):
        if not cls._isistenc:
            cls._isistenc = super(View, cls).__new__(cls)
        return cls._isistenc

    def __init__(self) -> None:
        self.st_data = []

    def prepare_data_st(self, data: Students):
        student_order = {"Очередь": 0, "Сдал": 1, "Провалил": 2}

        if not self.st_data:
            for student in data.data:
                self.st_data.append(
                    (data.data[student].get_name, data.data[student].get_resault)
                )
                self.st_data.sort(key=lambda x: student_order[x[1]])
            return
        for i in range(len(self.st_data)):
            if data.data[self.st_data[i][0]].get_resault != self.st_data[i][1]:
                self.st_data[i] = (
                    data.data[self.st_data[i][0]].get_name,
                    data.data[self.st_data[i][0]].get_resault,
                )
        self.st_data.sort(key=lambda x: student_order[x[1]])

    def print_status(self, students: Students):
        self.prepare_data_st(students)
        print(f"     Статистика студентов     ")
        print(f"+--------------+-------------+")
        print(f"|  Студент     |  Статус     |")
        print(f"+--------------+-------------+")
        for item in self.st_data:
            print("|  %-11s |  %-10s |" % item)
        print(f"+--------------+-------------+")

    def print_status2(self, students: Students):
        print(f"     Статистика студентов     ")
        print(f"+--------------+-------------+")
        print(f"|  Студент     |  Статус     |")
        print(f"+--------------+-------------+")
        for student in students.data:
            print(
                "|  %-11s |  %-10s |"
                % (students.data[student].get_name, students.data[student].get_resault)
            )
        print(f"+--------------+-------------+")

    def print_status_monitor(self, examinators: Examinators):
        print("\n\n")
        print(f"                     Cтатус хода экзамена                      ")
        print(
            f"+--------------+------------------+------------------+-----------+---------------+"
        )
        print(
            f"|  Экзаменатор | Текущий студент  |  Всего студентов |  Завалил  |  Время работы |"
        )
        print(
            f"+--------------+------------------+------------------+-----------+---------------+"
        )
        for i in examinators:
            print(
                "| %-6s       |  %-12s    |       %-3s        |     %-3s   |   %-5s сек   |"
                % (i.name, i.curent_student, i.student_ct, i.st_filed, i.time)
            )
        print(
            f"+--------------+------------------+------------------+-----------+---------------+"
        )

    def for_deduction(slef, examinators: Examinators):
        failed_students = []
        for teacher in examinators.examinators:
            failed_students.extend(teacher.failed_student)
        if not failed_students:
            return "-"
        else:
            if len(failed_students) == 1:
                return failed_students[0].get_name
            else:
                failed_students.sort(key=lambda x: x.exam_time)
                return failed_students[0].get_name

    def print_end_status_monitor(self, examinators: Examinators):
        print("\n")
        print(f"                            Итоги экзамена                      ")
        print(f"+--------------+------------------+------------------+---------------+")
        print(f"|  Экзаменатор | Всего студентов  |  Завалил         |  Время работы |")
        print(f"+--------------+------------------+------------------+---------------+")
        for i in examinators.examinators:
            print(
                "| %-6s       |  %-12s    |       %-3s        |   %-5s сек   |"
                % (i.name, len(i.student_conut), len(i.failed_student), i.time)
            )
        print(f"+--------------+------------------+------------------+---------------+")

    def print_end_stat(self, stud: Students, examinators: Examinators, q: Qestions):
        min_time = float("inf")
        best_student = None
        for i in stud.data:
            if stud.data[i].exam_time < min_time and stud.data[i].resault != "Провалил":
                min_time = stud.data[i].exam_time
                best_student = stud.data[i]
        best_examinators = ""
        for teacher in examinators.examinators:
            if teacher.zavalil == 0:
                best_examinators = (
                    best_examinators + f", {teacher.name}"
                    if best_examinators
                    else teacher.name
                )
        self.for_deduction(examinators)

        failed_students_ct = 0
        for i in examinators.examinators:
            failed_students_ct += len(i.failed_student)
        resault_exam = (
            "Экзамен удался"
            if 100 - (failed_students_ct / len(stud.data) * 100) >= 85
            else "Экзамен не удался"
        )
        print(
            f"Имена лучших студентов: {best_student.get_name}\n"
            f"Имена лучших экзаменаторов: {best_examinators}\n"
            f"Имена студентов которых отчислять после экзамена: {self.for_deduction(examinators)}\n"
            f"Лучшие вопросы: {q.best_questions(len(stud.data))}\n"
            f"Вывод: {resault_exam}"
        )


if __name__ == "__main__":
    ex = Examinators()
    ex.print()
    print(ex.examinators)
    print(ex.teacher_choos("Программирование интересеное занятие", ex.examinators[0]))
    print(ex.teacher_choos("Программирование интересеное занятие", ex.examinators[1]))

    vi = View()
    vi.print_end_stat()
