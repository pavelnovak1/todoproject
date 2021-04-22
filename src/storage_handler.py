import to_do_storage as storage
import pickle
DATAFILE = "./data/"

def load(name):
    """
    Loads data from file. If file does not exist, creates a new one.
    :param name: Filename specificator
    :return: Loaded To Do list. None, if a new file was created.
    """
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
    """
    Save to do list into the file.
    :param tdlist: To Do list to save.
    :param name: Filename specificator.
    :return: None.
    """
    with open(DATAFILE + f"{name}.data", "wb") as file:
        pickle.dump(tdlist, file)

