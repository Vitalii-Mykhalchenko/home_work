from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        if len(phone) == 10 and phone.isdigit():
            self.value = phone
        else:
            raise ValueError()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, delete):
        result = list(
            filter(lambda el: el.value != delete, self.phones))
        if len(result) != len(self.phones):
            self.phones = result
        else:
            print("This phone is not in list")

    def edit_phone(self, phone, new_phone):
        for el in self.phones:
            if el.value == phone:
                self.remove_phone(phone)
                self.add_phone(new_phone)
                break
            else:
                raise ValueError("This phone not found")

    def find_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                return el

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    # def __init__(self): ця функція за замовчуванням унаслідує від нащадка
    #     self.data = {}

    def add_record(self, phone: Record):
        self.data[phone.name.value] = phone

    def find(self, name):
        for key, value in self.data.items():
            if key == name:
                return value

    def delete(self, name):
        try:
            del self.data[name]
        except KeyError:
            print("this name not in list")
