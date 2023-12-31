from datetime import datetime
from collections import UserDict
import csv
import os


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


class Name(Field):
    # def __init__(self, name):
    # self.value = name
    pass


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    @Field.value.setter
    def value(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError
        self._value = value


class Birthday(Field):
    def __init__(self, string=None):
        super().__init__(string)

    @Field.value.setter
    def value(self, value: str = None):
        if value:
            self._value = datetime.strptime(value, "%d.%m.%Y")


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
            return None
        today = datetime.now()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        days_until = (next_birthday - today).days
        return f" {days_until} days until the next birthday"

    def __str__(self):
        return f"Contact name: {self.name.value},  phones: {'; '.join(p.value for p in self.phones)},  birthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self, data=None):
        self._file_name = "contacts.csv"
        self._isFile = os.path.isfile(self._file_name)
        super().__init__(data if data is not None else self.restore_data())

    def add_record(self, phone: Record):
        self.data[phone.name.value] = phone
        self.write_contacts_to_file(phone)

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

    def write_contacts_to_file(self, phone: Record):
        self._isFile = os.path.isfile(self._file_name)
        name = phone.name.value
        phones = ",".join([phone.value for phone in phone.phones])
        birthday = str(phone.birthday.value.date().strftime("%d.%m.%Y")
                       ) if phone.birthday.value else None
        header = ["name", "phone", "birthday"]

        isContactExist = False

        if self._isFile:
            with open(self._file_name, "r", newline="")as file:
                read = csv.DictReader(file)
                for contact in read:
                    contact_name = contact["name"]
                    contact_phone = contact["phone"]
                    contact_birthday = contact["birthday"] if contact["birthday"] != "" else None

                    if name == contact_name and phones == contact_phone and birthday == contact_birthday:
                        isContactExist = True
                        break

        with open(self._file_name, "a", newline="")as file:
            writer = csv.DictWriter(file, fieldnames=header)
            if not self._isFile:
                writer.writeheader()

            if not isContactExist:
                writer.writerow({
                    "name": name,
                    "phone": phones,
                    "birthday": birthday
                })

    def restore_data(self):
        result = {}
        if self._isFile:
            with open(self._file_name, "r", newline="")as file:
                read = csv.DictReader(file)
                for row in read:
                    name = row["name"]
                    phones = list(filter(None, row["phone"].split(",")))
                    birthday = row["birthday"]

                    new_record = Record(name, birthday)
                    for phone in phones:
                        new_record.add_phone(phone)
                    result.update({name: new_record})
        return result

    def find_from_csv(self, target_name):
        target_name = target_name.lower()
        data = list(self.data.values())

        def lam(elem: Record):
            name = elem.name.value
            name = name.lower()
            phone = elem.phones
            is_phone = False

            for el in phone:
                if target_name in el.value:
                    is_phone = True
                    break
                
            is_name = target_name in name    
            return is_name or is_phone
            
        result_find = list(filter(lam,  data))
        if len (result_find) == 0:
            return "Not Found"
        

        result_all_contact = ""
        for el in result_find:
            result_all_contact += f"{el} \n"
        return result_all_contact

