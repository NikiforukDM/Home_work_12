from collections import UserDict
from datetime import datetime
import pickle


def _create_date(*, year, month, day):
    return datetime(year=year, month=month, day=day).date()


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, num):
        number = ''
        for n in num:
            try:
                n = int(n)
                number += str(n)

            except ValueError:
                None
        if len(number) == 12 and number[0:3] == '380':
            self._value = number
        elif len(number) == 10 and number[0] == '0':
            self._value = f'38{number}'
        elif len(number) == 11 and number[0:2] == '80':
            self._value = f'3{number}'
        else:
            print('Number is not validate')
            self._value = ''


class Birthday(Field):

    @property
    def value(self) -> datetime.date:
        return self._value

    @value.setter
    def value(self, value):

        if value is None:
            return None
        else:
            try:
                self._value = datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                print('Birthday format must be 00-00-000')
                return None

    def __repr__(self):
        return datetime.strftime(self._value, "%d-%m-%Y")


class AddressBook(UserDict):
    __book_name = "address_book.pickle"

    def __enter__(self):
        self.__restore()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save()

    def __restore(self):
        try:
            with open(self.__book_name, "rb+") as file:
                book = pickle.load(file)
                self.data.update(book)
        except Exception:
            print("Book is not restored!")

    def __save(self):
        try:
            with open(self.__book_name, "wb+") as file:
                pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)
                print("Book saved!")
        except Exception:
            print("Some problems!")

    limit = 5
    offset = 0

    def __next__(self):
        self.addresses = list(self.data.items())
        end_value = self.offset + self.limit
        page = self.addresses[self.offset:end_value]
        self.offset = end_value
        if self.offset > len(self.addresses):
            page = self.addresses[end_value -
                                  self.limit:len(self.addresses)+1]

        if page == []:
            print('No more addresses')

        return page

    def __repr__(self):
        string = ''
        for name, other_data in self.data.items():
            string = string + f"{self.data[name]}\n"
        return string

    def add_contact(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        contact = Record(name=name, phone=phone, birthday=birthday)
        if name.value in self.data.keys():
            print(f'Name {name.value.capitalize()} is in the book already! Try another name.')
            return None
        else:
            self.data[name.value] = contact


    def add_record(self, record: "Record"):
        self.data[record.name.value] = record

    def find_coincidence(self,part_word):
        coincidence = []
        for record in self.data.values():
            if part_word in str(record.name.value) or part_word in str([phone.value for phone in record.phones]):
                coincidence.append(record)

        print(f'Your addresses are {coincidence}')


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name: Name = name
        self.phones: list[Phone] = [phone] if phone is not None else []
        self.birthday = birthday

    def __repr__(self):
        if self.birthday == None or self.birthday.value == None:
            return f'{self.name.value.capitalize()} : {" ".join(phone.value for phone in self.phones)}'
        return f'{self.name.value.capitalize()}: {" ".join(phone.value for phone in self.phones)} : {self.birthday.value.date()}'

    def days_to_birthday(self):
        now = datetime.today().date()
        if self.birthday is not None:
            birthday: datetime = self.birthday.value.date()
            next_birthday = _create_date(
                year=now.year, month=birthday.month, day=birthday.day)
            if now > next_birthday:
                next_birthday = _create_date(
                    year=next_birthday.year + 1, month=next_birthday.month, day=next_birthday.day)
            print(f'{(next_birthday-now).days} days')
            return (next_birthday-now).days
        return None

    def add_phone(self, phone_number: Phone):
        self.phones.append(phone_number)

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def change_phone(self, old_number: str, new_number: Phone):
        try:

            for ph in self.phones:
                if ph.value == old_number:
                    self.phones.remove(ph)
                    self.phones.append(new_number)
                else:
                    print(f'Phone {old_number} does not exists')
                return self.phones
        except ValueError:
            print(f'{old_number} does not exists')

    def delete_phone(self, phone: Phone):

        # try:
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)
                return self.phones
        print(f'Number {phone} does not exists')
