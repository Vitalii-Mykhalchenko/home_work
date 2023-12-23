from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def set_value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


class Name(Field):
    # def __init__(self, name):
    # self.value = name
    pass


class Phone(Field):
    def __init__(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError()
        super().__init__(phone)

    @Field.value.setter
    def set_value(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError
        self._value = value


class Birthday(Field):
    def __init__(self, string):
        if string is None:
            super().__init__(string)
        else:
            data = datetime.strptime(string, '%d.%m.%Y')
            super().__init__(data)

    @Field.value.setter
    def set_value(self, value: str):
        self.value = datetime.strptime(value, '%d.%m.%Y')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

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

    def days_to_birthday(self):
        print(self.birthday)
        if self.birthday.value is None:
            print("!!!!!!!!!!")
            return None
        today = datetime.now()
        next_birthday = self.birthday.value.replace(year=today.year)
        # Якщо день народження вже минув у цьому році, додаємо 1 рік
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        # Обчислюємо різницю між сьогоднішньою датою та наступним днем народження
        days_until = (next_birthday - today).days
        return f" {days_until} days until the next birthday"

    def __str__(self):
        return f"Contact name: {self.name.value},  phones: {'; '.join(p.value for p in self.phones)},  birthday: {self.birthday}"


class AddressBook(UserDict):

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

    def iterator(self, index=1):
        my_dict = self.data
        dict_len = len(self.data)
        page_size = 10
        values_list = list(my_dict.values())
        pages = [values_list[i:i + page_size]
                 for i in range(0, len(values_list), page_size)]
        start_page = index - 1
        end_page = index
        curent_page = next(iter(pages[start_page:end_page]), [])

        result = f"Page {index} \n"

        for record in curent_page:
            result += f"{record} \n"
        return result
