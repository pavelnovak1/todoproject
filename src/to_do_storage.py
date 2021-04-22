import datetime
from hashlib import sha224


class ToDoItem:
    __title: str
    __deadline: datetime.date
    __importance: int

    def __init__(self, title, deadline, importance):
        self.__title = title
        self.__deadline = deadline
        self.__importance = importance

    def __str__(self):
        return f"{self.__title} must be done before {self.__deadline}. It's importance is {self.__importance}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__title == other.__title
        return False

    def __hash__(self):
        return hash(self.__title)

    def is_after_deadline(self):
        return self.__deadline < datetime.date()

    def is_important(self):
        return self.__importance >= 4

    def get_title(self):
        return self.__title

    def get_deadline(self):
        return self.__deadline

    def get_importance(self):
        return self.__importance


class ToDoList:

    def __init__(self, master_pwd):
        self.__storage = []
        self.__master_password = sha224(master_pwd.encode("utf-8")).hexdigest()

    def add_item(self, title, deadline: datetime.datetime, importance):
        if deadline < datetime.datetime.now():
            raise RuntimeError("Item's deadline already expired")

        item = ToDoItem(title, deadline, importance)
        if item in self.__storage:
            raise RuntimeError("Item is already present in To Do list")

        self.__storage.append(item)
        return True

    def get_item_by_title(self, title):
        for item in self.__storage:
            if item.get_title() == title:
                return item
        return None

    def get_items_by_deadline(self, deadline):
        results = []
        for item in self.__storage:
            if item.get_deadline() == deadline:
                results.append(item)
        return results

    def get_nearest_deadline(self):
        if len(self.__storage) == 0:
            return None
        nearest = self.__storage[0]
        for item in self.__storage:
            if item.get_deadline < nearest.get_deadline():
                nearest = item
        return nearest

    def get_all(self):
        return self.__storage

    def has_item(self, title):
        for item in self.__storage:
            if item.get_title == title:
                return True
        return False

    def verify_passwd(self, passwd):
        return sha224(passwd.encode("utf-8")).hexdigest() == self.__master_password




