import sys, datetime
import to_do_storage as storage
from storage_handler import load, save


def print_menu():
    print("1 - Add new item")
    print("2 - Find item by name")
    print("3 - Find by nearest deadline")
    print("4 - Edit item")
    print("5 - Delete item")
    print("6 - End")

def add_item(tdlist: storage.ToDoList):
    title = input("Title: ")
    if tdlist.has_item(title):
        print("This item is already in to do list.")
        return False
    deadline_year = int(input("Deadline year: "))
    deadline_month = int(input("Deadline month (1 - 12): "))
    deadline_day  = int(input("Deadline day: "))
    deadline = datetime.datetime(deadline_year, deadline_month, deadline_day)
    importance = int(input("Importance (1 - Low, 5 - High"))
    tdlist.add_item(title, deadline, importance)
    return True


def find_item_name(tdlist: storage.ToDoList):
    title = input("Title: ")
    item = tdlist.get_item_by_title(title)
    if item:
        print(f"Title: {title}")
        print(f"Deadline: {item.get_deadline()}")
        print(f"Importance: {item.get_importance()}")
        return True
    else:
        print("No such item.")
        return False


def find_nearest_deadline(tdlist: storage.ToDoList):
    all_items = tdlist.get_all()
    if len(all_items) == 0:
        print("No item in To Do list.")
        return False
    else:
        min = all_items[0]
        for item in all_items:
            if item.get_deadline() < min.get_deadline():
                min = item
        print(f"Title: {min.get_title()}")
        print(f"Deadline: {min.get_deadline()}")
        print(f"Importance: {min.get_importance()}")
        return True


def delete_item(tdlist: storage.ToDoList):
    all_items = tdlist.get_all()
    if len(all_items) == 0:
        print("To Do list is empty.")
    title = input("Title: ")
    item = tdlist.get_item_by_title(title)
    if item:
        index = all_items.index(item)
        all_items.pop(index)
        return True
    print(f"No item with name {title}")
    return False


def main():
    master_pwd = sys.argv[3]
    to_do_list = load(sys.argv[2])
    if not to_do_list:
        to_do_list = storage.ToDoList(master_pwd)

    if not to_do_list.verify_passwd(master_pwd):
        print("Wrong master password")
        sys.exit()
    end = False
    while not end:
        print_menu()
        choice = int(input())
        if choice == 1:
            add_item(to_do_list)
        elif choice == 2:
            find_item_name(to_do_list)
        elif choice == 3:
            find_nearest_deadline(to_do_list)
        elif choice == 4:
            print("Not implemented yet")
        elif choice == 5:
            delete_item(to_do_list)
        elif choice == 6:
            save(to_do_list)
            exit()
        else:
            print(f"Unknown choice {choice}. Try again.")

