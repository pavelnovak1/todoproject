import to_do_storage as storage
import pickle
DATAFILE = "./data/"

def load(name):
    to_do_list: storage.ToDoList = None
    try:
        with open(DATAFILE + f"{name}.data", "rb") as data:
            to_do_list = pickle.load(data)

    except FileNotFoundError:
        with open(DATAFILE + f"{name}.data", "w"):
            pass
    except:
        print("Error while loading data")
    return to_do_list

def save(tdlist: storage.ToDoList, name):
    with open(DATAFILE + f"{name}.data", "wb") as file:
        pickle.dump(tdlist, file)

