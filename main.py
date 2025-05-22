# Базовый класс для людей (пациентов и врачей)
class Human:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_data(self):
        print(self.first_name, self.last_name)


# Класс для пациентов наследуется от Human
class Patient(Human):
    def __init__(self, first_name, last_name, priority_pass, doctor_id):
        super().__init__(first_name, last_name)
        self.priority_pass = priority_pass
        self.meeting_time = None
        self.patient_id = None
        self.number_in_queue = None
        self.doctor_id = doctor_id


# Класс для врачей тоже наследуется от Human
class Doctor(Human):
    def __init__(self, first_name, last_name, doctor_id, room):
        super().__init__(first_name, last_name)
        self.doctor_id = doctor_id
        self.room = room


# Класс для управления очередью пациентов
class QueueManager:
    def __init__(self):
        self.list_of_patients = []
        self.next_patient_id = 1

    # Добавляет пациента в очередь
    def add_patient(self, patient):
        patient.patient_id = self.next_patient_id
        patient.number_in_queue = len(self.list_of_patients) + 1
        self.list_of_patients.append(patient)
        self.next_patient_id += 1
        print(f"Пациент добавлен. Номер в очереди: {patient.number_in_queue}, ID: {patient.patient_id}")

    # Удаляет пациента из очереди по ID и имени
    def remove_patient(self, id=None, first_name=None, last_name=None):
        for patient in self.list_of_patients:
            if (id and patient.patient_id == id) or (
                first_name and last_name and patient.first_name == first_name and patient.last_name == last_name):
                self.list_of_patients.remove(patient)
                print("Пациент удалён.")
                break
        else:
            print("Пациент не найден.")

        for i, patient in enumerate(self.list_of_patients, start=1):
            patient.number_in_queue = i

    # Показывает текущую очередь
    def view_queue(self):
        if not self.list_of_patients:
            print("Очередь пуста.")
            return
        for patient in self.list_of_patients:
            print(
                f"{patient.number_in_queue}) {patient.first_name} {patient.last_name} | ID: {patient.patient_id} | Приоритет: {patient.priority_pass} | Время: {patient.meeting_time}"
            )

    # Меняет время приёма для пациента
    def retime_patient(self, id=None, first_name=None, last_name=None):
        for patient in self.list_of_patients:
            if (id and patient.patient_id == id) or (
                first_name and last_name and patient.first_name == first_name and patient.last_name == last_name
            ):
                new_time = input("Введите новое время приёма (например, 12:30): ")
                patient.meeting_time = new_time
                print("Время приёма обновлено.")
                return
        print("Пациент не найден.")

    # Вызывает следующего пациента из очереди
    def call_next_patient(self):
        if not self.list_of_patients:
            print("Очередь пуста.")
            return
        next_patient = self.list_of_patients.pop(0)
        print(
            f"Следующий пациент: {next_patient.first_name} {next_patient.last_name} (ID: {next_patient.patient_id})"
        )
        for i, patient in enumerate(self.list_of_patients, start=1):
            patient.number_in_queue = i


#словарь с врачами
doctors = {
    1: Doctor("Иван", "Иванов", 1, 101),
    2: Doctor("Петр", "Петров", 2, 102),
    3: Doctor("Сергей", "Сергеев", 3, 103),
}

#Для каждого врача своя очередь
queues = {doc_id: QueueManager() for doc_id in doctors}


# Основной цикл с меню для взаимодействия
while True:
    print("\nДобро пожаловать в электронную очередь! Выберите нужное вам действие:")
    print("1) Записаться к врачу")
    print("2) Посмотреть очередь")
    print("3) Удалить запись")
    print("4) Перенести запись")
    print("5) Вызвать следующего пациента")
    print("0) Выйти")

    choice = input("Введите номер действия: ")

    # Обработка записи к врачу
    if choice == "1":
        print("Выберите врача:")
        for doc_id, doc in doctors.items():
            print(f"{doc_id}) {doc.first_name} {doc.last_name} (Кабинет: {doc.room})")
        doc_choice = int(input("Введите номер врача: "))
        if doc_choice not in doctors:
            print("Неверный выбор врача.")
            continue

        fname = input("Введите имя пациента: ")
        lname = input("Введите фамилию пациента: ")
        is_pensioner = input("Вы пенсионер? (Да/Нет): ").lower() == "Да"
        with_children = input("Вы с детьми? (Да/Нет): ").lower() == "Да"
        priority = is_pensioner or with_children
        new_patient = Patient(fname, lname, priority, doctor_id=doc_choice)
        queues[doc_choice].add_patient(new_patient)

    # Показ очереди для выбранного врача
    elif choice == "2":
        doc_choice = int(input("Введите ID врача для просмотра очереди: "))
        if doc_choice in queues:
            queues[doc_choice].view_queue()
        else:
            print("Такого врача нет.")

    # Удаление пациента из очереди
    elif choice == "3":
        doc_choice = int(input("Введите ID врача: "))
        fname = input("Имя пациента: ")
        lname = input("Фамилия пациента: ")
        queues[doc_choice].remove_patient(first_name=fname, last_name=lname)

    # Изменение времени приёма
    elif choice == "4":
        doc_choice = int(input("Введите ID врача: "))
        fname = input("Имя пациента: ")
        lname = input("Фамилия пациента: ")
        queues[doc_choice].retime_patient(first_name=fname, last_name=lname)

    # Вызов следующего пациента
    elif choice == "5":
        doc_choice = int(input("Введите ID врача: "))
        queues[doc_choice].call_next_patient()

    # Выход из программы
    elif choice == "0":
        print("Выход...")
        break

    # неверный ввод
    else:
        print("Неверный выбор. Повторите.")