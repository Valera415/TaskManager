import json
from typing import List


COMMANDS = {
    1: 'Просмотр задач',
    2: 'Добавление задачи',
    3: 'Изменение задачи',
    4: 'Удаление задачи',
    5: "Поиск задач",
    0: 'Выход',
}

PRIORITY = {
    1: "Низкий приоритет",
    2: "Средний приоритет",
    3: "Высокий приоритет",
}


class Task:
    DEFAULT_STATUS = "Не выполнена"
    ALT_STATUS = "Выполнена"

    def __init__(self, id: int, title: str, description: str, category: str, date: str, priority: str, status: str = DEFAULT_STATUS):
        # Для упрощения использования id делается автоматически из последнего элемента списка задач, но это не лучший вариант
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.date = date
        self.priority = priority
        self.status = status

    def change_status(self):
        """Меняет статус задачи"""
        self.status = self.ALT_STATUS if self.status == self.DEFAULT_STATUS else self.DEFAULT_STATUS

    def __str__(self):
        return f"ID: {self.id}, Название: {self.title}, Описание: {self.description}, Категория: {self.category}, Срок: {self.date}, Приоритет: {self.priority}, Статус: {self.status}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def _get_task_input(self):
        """Собирает данные для новой задачи от пользователя"""
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        category = input("Введите категорию: ")
        date = input("Введите дату: ")
        print("Выберите приоритет задачи: ")
        for key, value in PRIORITY.items():
            print(f"{key}: {value}")
        try:
            priority = PRIORITY[int(input())]
        except:
            print("Неверный приоритет задачи")
            return None
        return title, description, category, date, priority

    def add_task(self, title: str, description: str, category: str, date: str, priority: str):
        """Добавляет новую задачу"""
        if not (title and description and category and date):
            print("Пропущено одно из полей")
            return
        id = self.tasks[-1].id + 1 if self.tasks else 1
        new_task = Task(id, title, description, category, date, priority)
        self.tasks.append(new_task)

    def add_task_interactive(self):
        """Добавление задачи через интерфейс"""
        new_task_data = self._get_task_input()
        if new_task_data:
            self.add_task(*new_task_data)
        else:
            print("Не удалось добавить задачу")

    def remove_task_by_id(self, id: int):
        """Удаляет задачу по id"""
        task = self.find_task(id)
        if task:
            self.tasks.remove(task)
            print("Задача удалена")
        else:
            print("Задача с таким ID не найдена")

    def find_task(self, search_id: int):
        """Находит задачу по ID"""
        for task in self.tasks:
            if task.id == search_id:
                return task
        return None

    def search_tasks(self, title: str = None, description: str = None, category: str = None, date: str = None):
        """Ищет задачи по критериям"""
        results = [
            task for task in self.tasks
            if (not title or title.lower() in task.title.lower()) and
               (not description or description.lower() in task.description.lower()) and
               (not category or category.lower() == task.category.lower()) and
               (not date or date == task.date)
        ]
        return results

    def show_tasks(self):
        """Выводит все задачи или задачи по категории"""
        choice = input(
            "1. Показать все задачи\n"
            "2. Показать задачи по категории\n"
            "0. Назад\n"
        )

        match choice:
            case "1":
                if self.tasks:
                    print("Все задачи:")
                    for task in self.tasks:
                        print(task)
                else:
                    print("Список задач пуст.")
            case "2":
                category = input("Введите категорию: ")
                tasks_by_category = self.search_tasks(category=category)
                if tasks_by_category:
                    print(f"Задачи в категории '{category}':")
                    for task in tasks_by_category:
                        print(task)
                else:
                    print(f"Задач в категории '{category}' не найдено.")
            case "0":
                return
            case _:
                print("Неверный выбор")

    def process_command(self, command: str):
        """Обрабатывает пользовательский ввод"""
        match command:
            case "1":
                self.show_tasks()
            case "2":
                self.add_task_interactive()
            case "3":
                id = int(input("Введите ID задачи: "))
                task = self.find_task(id)
                if not task:
                    print("Задача с указанным ID не найдена")
                else:
                    print(task)
                    user_choice_in_case = input(
                        "1. Изменить статус задачи\n"
                        "2. Редактировать\n"
                        "0. Назад\n")
                    match user_choice_in_case:
                        case "1":
                            task.change_status()
                        case "2":
                            new_attr = self._get_task_input()
                            if new_attr:
                                task.title, task.description, task.category, task.date, task.priority = new_attr
                        case "0":
                            return
                        case _:
                            print("Неверная опция")
            case "4":
                id_to_remove = int(input("Введите ID задачи для удаления: "))
                self.remove_task_by_id(id_to_remove)
            case "5":
                title = input("Название (оставьте пустым для пропуска): ")
                description = input("Описание (оставьте пустым для пропуска): ")
                category = input("Категория (оставьте пустым для пропуска): ")
                date = input("Дата (оставьте пустым для пропуска): ")
                results = self.search_tasks(title, description, category, date)
                if results:
                    print("Найденные задачи:")
                    for task in results:
                        print(task)
                else:
                    print("Задачи не найдены.")
            case "0":
                return False
            case _:
                print("Неверный выбор")
        return True


class Storage:
    @staticmethod
    def load_data(file_path: str) -> List[Task]:
        """Загружает данные из json файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)
                data = [Task(**item) for item in raw_data]
                return data
        except:
            print("Не найден data.json, будет создан новый")
            return []

    @staticmethod
    def save_data(file_path: str, tasks: List[Task]):
        """Сохраняет данные в JSON файл"""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([task.__dict__ for task in tasks], file, ensure_ascii=False, indent=2)


def main():
    task_manager = TaskManager()
    task_manager.tasks = Storage.load_data("data.json")

    while True:
        print("\nМеню:")
        for key, value in COMMANDS.items():
            print(f"{key}: {value}")
        user_choice = input("Введите номер опции: ")

        if not task_manager.process_command(user_choice):
            break

    Storage.save_data("data.json", task_manager.tasks)
    print("Данные сохранены. Выход.")


if __name__ == "__main__":
    main()
