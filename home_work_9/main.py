CONTACTS = {}


def add_contact(name, phone):
    CONTACTS[name] = phone
    print(f"Contact {name} added with phone number {phone}")


def change_contact(name, phone):
    if name in CONTACTS.keys():
        CONTACTS[name] = phone
        print(f"Phone number for {name} changed to {phone}.")
    else:
        print(f"{name} does not exist")


def phone_number(name):
    if name in CONTACTS.keys():
        print(f"The phone number for '{name}' is {CONTACTS[name]}")
    else:
        print(f"Contact '{name}' not found.")


def show_all_contacts():
    if len(CONTACTS) == 0:
        print("No contacts")
    else:
        print(
            "\n".join([f"{name}: {phone}" for name, phone in CONTACTS.items()]))


def say_hello():
    print("Hello user")


def say_bye():
    print("Bye, see you later")
    exit()


COMMANDS = {
    'hello': say_hello,
    'add': add_contact,
    'change': change_contact,
    'phone': phone_number,
    'show all': show_all_contacts,
    'good bye': say_bye,
    'close': say_bye,
    'exit': say_bye,
}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            print(f"Input error: {str(e)}")

    return wrapper


@input_error
def main():
    while True:
        user_input = input("Enter a command: ")
        for comm, handler in COMMANDS.items():
            if user_input.lower().startswith(comm):
                payload = user_input[len(comm):].split()
                if len(payload) > 2:
                    print("Wrong number of arguments")
                    continue
                if len(payload) > 1:
                    el_1, el_2 = payload
                    handler(el_1, el_2)
                    break
                elif len(payload) == 1:
                    el_1 = payload[0]
                    handler(el_1)
                    break
                else:
                    handler()
                    break
        else:
            print("Invalid command, try again with a correct one")


if __name__ == "__main__":
    main()
