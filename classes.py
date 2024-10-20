from collections import UserDict
import re
from datetime import datetime, timedelta

class ValidationError(Exception):
    pass

class NotFoundError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
		pass


class Phone(Field):
    def __init__(self, value: str):
        if self.is_phone_valid(value):
                self.value = value

        else:
            raise ValidationError("Incorrect phone number. Use 10 numbers")
        
    def is_phone_valid(self, phone: str) -> bool:
        return bool(re.fullmatch(r"\d{10}", phone))


class Birthday(Field):
    def __init__(self, value: str):
        if self.is_date_valid(value):
                self.value = datetime.strptime(value, "%d.%m.%Y").date()

        else:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")
        
    def is_date_valid (self, date: str) -> bool:
        date_pattern = r"^(0[1-9]|[12]\d|3[01]).(0[1-9]|1[0-2]).\d{4}$"
        return re.match(date_pattern, date)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)

        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_phone_obj = self.find_phone(old_phone)

        if old_phone_obj:
            new_phone_obj = Phone(new_phone)
            index = self.phones.index(old_phone_obj)
            self.phones[index] = new_phone_obj
            
    def find_phone(self, phone: str) -> Phone:
        searched_phone = next((p for p in self.phones if p.value == phone), None)

        if not searched_phone:
            raise NotFoundError(f"No such phone number: {phone} in the list for {self.name}")

        return searched_phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def get_upcoming_birthdays (self) -> list[dict]:
        upcoming_birthdays = []
        current_date = datetime.today().date()
        current_year = datetime.now().year
        target_date = current_date + timedelta(days=7)

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=current_year)

                if current_date <= birthday_this_year <= target_date:
                    congratulation_info = {
                        "name": record.name.value,
                        "birthday": record.birthday.value.strftime("%d.%m.%Y")
                    }
                    weekday = birthday_this_year.weekday()

                    if weekday < 5:
                        congratulation_info["congratulation_date"] = birthday_this_year.strftime("%d.%m.%Y")
                    else:
                        congratulation_info["congratulation_date"] = (birthday_this_year + timedelta(days=(7-weekday))).strftime("%d.%m.%Y")

                    upcoming_birthdays.append(congratulation_info)
   
        return upcoming_birthdays
