import pickle
from pathlib import Path
from classes import AddressBook

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    file_path = Path(filename)

    if file_path.exists():
        with open(filename, "rb") as file:
            return pickle.load(file)
        
    return AddressBook()