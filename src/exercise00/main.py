from concurrent.futures import ThreadPoolExecutor as TPE
import time
from random import uniform
import asyncio
from s21.file import *
from time import sleep
import os
import threading

printLock = threading.Lock()


def decision(student: Student, teacher: Examinator, max_bal):
    mood = random()
    if mood <= 1 / 8:
        student.resault = "Провалил"
        teacher.failed_student.append(student)
        teacher.zavalil += 1
    elif 1 / 4 <= mood > 1 / 8:
        student.resault = "Сдал"
    else:
        if (max_bal // 2) < student.bal:
            student.resault = "Сдал"
        else:
            student.resault = "Провалил"
            teacher.failed_student.append(student)
    teacher.student_conut.append(student.name)


class Runner:
    def __new__(cls):
        if not hasattr(cls, "_obj"):
            cls._obj = super(Runner, cls).__new__(cls)
        return cls._obj

    def __init__(self):
        self.students = Students()
        self.teachers = Examinators()
        self.questions = Qestions()
        self.v = View()
        self._len_quee = 0
        self.quee = []
        self.timer = 0
        self.timer_for_break = 0

    @property
    def len_quee(self):
        self._len_quee -= 1
        return self._len_quee

    @len_quee.setter
    def len_quee(self, len):
        self._len_quee = len

    def make_quee(self):
        tech_ct = 0
        ls_student = [i for i in self.students.data]
        tmp = []
        for s in range(len(ls_student)):
            if tech_ct >= len(self.teachers.examinators):
                tech_ct = 0
                self.quee.append(tmp)
                tmp = []
            self.teachers.examinators[tech_ct].curent_student = "-"
            tmp.append(
                (self.students.data[ls_student[s]], self.teachers.examinators[tech_ct])
            )
            # self.quee.append((self.students.data[ls_student[s]], self.teachers.examinators[tech_ct]))
            tech_ct += 1
        self.quee.append(tmp)

    def make_quee2(self):
        temp = []
        pointer = 0
        ls_student = [i for i in self.students.data]
        stud_ct = len(ls_student) // len(self.teachers.examinators)

        for teacher in self.teachers.examinators:
            tmp = []
            for _ in range(stud_ct):
                tmp.append(self.exam(self.students.data[ls_student[pointer]], teacher))
                pointer += 1
            temp.append(tmp)
        while pointer < len(self.students.data):
            tmp.append(
                self.exam(
                    self.students.data[ls_student[pointer]],
                    self.teachers.examinators[-1],
                )
            )
            pointer += 1

        return temp

    def take_item(self):
        return self.quee.pop(0)

    def breakfast(self, stud: Student, teach: Examinator):
        teach.curent_student = "Обед"
        sl = randint(12, 18)
        with printLock:
            os.system("cls" if os.name == "nt" else "clear")
            self.v.print_status(self.students)
            self.v.print_status_monitor(self.teachers.examinators)
            print(
                f"\nВремя с начала экзамена: {round(time.time() - self.timer)} сек.\n"
                f"Осталось студентов в очреди: {self._len_quee}"
            )
        sleep(sl)
        teach.curent_student = stud.name

    async def exam(self, stud: Student, teach: Examinator):
        if teach.time_for_braek == 0:
            teach.time_for_braek = time.time()
        len_name_th = uniform(
            len(teach.name) - 1, len(teach.name) + 1
        )  # задержка экзамена
        if time.time() - teach.time_for_braek >= 30:
            teach.time_for_braek = time.time()
            self.breakfast(stud, teach)

        teach.curent_student = stud.get_name
        with printLock:
            os.system("cls" if os.name == "nt" else "clear")
            self.v.print_status(self.students)
            self.v.print_status_monitor(self.teachers.examinators)
            print(
                f"\nВремя с начала экзамена: {round(time.time() - self.timer)} сек.\n"
                f"Осталось студентов в очреди: {self._len_quee}"
            )
        await asyncio.sleep(len_name_th)
        for qestion in self.questions.qusetions:
            if stud.i_choos(qestion) in Examinators.teacher_choos(qestion, teach):
                stud.bal += 1
                with printLock:
                    self.questions.dc_questions[qestion] = (
                        self.questions.dc_questions.get(qestion, 0) + 1
                    )
        decision(stud, teach, len(self.questions.qusetions))
        teach.time = round(time.time() - self.timer, 2)
        with printLock:
            os.system("cls" if os.name == "nt" else "clear")
            self.v.print_status(self.students)
            self.v.print_status_monitor(self.teachers.examinators)
            print(
                f"\nВремя с начала экзамена: {round(time.time() - self.timer)} сек.\n"
                f"Осталось студентов в очреди: {self.len_quee}"
            )
            stud.exam_time = round(time.time() - self.timer, 2)
        teach.curent_student = "-"

    async def run_exam_stream(self, corutine: list):
        for c in corutine:
            await c

    def run2(self):
        quee = self.make_quee2()
        self.len_quee = len(self.students.data)
        workers = 6
        self.timer = time.time()
        with printLock:
            os.system("cls" if os.name == "nt" else "clear")
            self.v.print_status(self.students)
            self.v.print_status_monitor(self.teachers.examinators)
            print(
                f"\nВремя с начала экзамена: {round(time.time() - self.timer)} сек.\n"
                f"Осталось студентов в очреди: {len(self.quee)}"
            )

        if len(quee) < workers:
            workers = len(quee)
        corutins = [self.run_exam_stream(i) for i in quee]

        with TPE(max_workers=workers) as worker:
            tasks = [worker.submit(self.start2, corutin) for corutin in corutins]

            for task in tasks:
                task.result()

        os.system("cls" if os.name == "nt" else "clear")
        self.v.print_status(self.students)
        self.v.print_end_status_monitor(self.teachers)

        print(f"Экзамен шел: { round(time.time() - self.timer)} сек.")
        self.v.print_end_stat(self.students, self.teachers, self.questions)

    def run(self):
        self.make_quee()
        self.len_quee = len(self.students.data)
        self.timer = time.time()
        self.v.print_status(self.students)
        self.v.print_status_monitor(self.teachers.examinators)
        print(
            f"\nВремя с начала экзамена:{round(time.time() - self.timer)} сек.\n"
            f"Осталось студентов в очреди: {self._len_quee}"
        )
        while self.quee:
            tmp = []
            for item in self.take_item():
                tmp.append(self.exam(item[0], item[1]))

            asyncio.run(Runner.start(tmp))
        print(f"Время выполнения: { round(time.time() - self.timer)}")

    @staticmethod
    async def start(corutine):
        await asyncio.gather(*corutine)

    @staticmethod
    def start2(corutine):
        asyncio.run(corutine)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    qw = Runner()
    qw.run2()
