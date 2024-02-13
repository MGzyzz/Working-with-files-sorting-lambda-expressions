import re


with open('./data.txt', 'r') as f:
    contact = []
    for line in f.readlines():
        data = line.replace('\n', '').split(', ')
        name = data[0]
        phone_numbers = [x.strip() for x in data[1:]]
        product = {
            'name': name,
            'phone': phone_numbers,
        }
        contact.append(product)


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def write_file(data):
    with open('./data.txt', 'w') as f:
        for entry in data:
            name = entry['name']
            phones = ', '.join(entry['phone'])
            f.write(f'{name}, {phones}\n')


def contact_user(contacts):
    return contacts


def check_words(check):
    if re.match(r'^[\d+-]+$', check):
        return check
    else:
        return print(
            "Действие невозможно так как введенный вами номер содержит букву или другой символ. Пожалуйста напишите номер повторно")


def check_numbers(check):
    if re.match(r'^[a-zA-Z]+$', check):
        return check
    else:
        return print("Действие невозможно так как введенный вами имя содержит цифры или другой символ. Пожалуйста напишите имя повторно")


def continue_user():
    choose = input("Вы точно хотите совершить это действие? y/n\n").lower()

    if choose == "y" or choose == "ok" or choose == "yes":
        return True
    else:
        print("Действие отменено!")
        return False


def contact_number():
    result = f'\n{"Name":<5}|{"Phone":>5}\n{"-" * 35}\n'
    contact_user(contact).sort(key=lambda x: x["name"])

    for name in contact_user(contact):
        phone_numbers = " ".join(name['phone'])
        result += f"{name['name']:<5}|{phone_numbers:>5}\n"
    return result


def find_user(find):
    user_find = get_contact(contact,find)
    if user_find:
            if user_find['name'] == find:
                return print(f"\nКонтакт найден:\nИмя: {user_find['name']}\nНомера: {' '.join(f'[{x + 1}] {n}' for x, n in enumerate(user_find['phone']))}\n")
    else:
        return print("Введеный вами контакт не существует. Попробуйте снова")


def add_user():
    add_name = input("Пожалуйста введите имя\n").capitalize()
    new_user = get_contact(contact,add_name)

    if not new_user:
        if check_numbers(add_name):
            add_phone = input("Введите номер телефона\n")
            if check_words(add_phone):
                new_contact = {"name": add_name, "phone": [add_phone]}
                contact_user(contact).append(new_contact)
                return print("Пользователь был успешно добавлен!")
    else:
        print("Пользователь с таким именнем существует")


def notFound():
    return print("Введеный вами контакт не существует. Попробуйте снова")


def add_phone():
    user = input("Пожалуйста введите имя контакта\n").capitalize()
    new_user = get_contact(contact, user)
    find_user(user)

    if new_user:
        add_number = input("\nВведите номер для добавление\n")
        if check_words(add_number):
            new_user['phone'].append(add_number)
            return print("Номер успешно добавлен!")


def get_contact(contact_list: list, name) -> dict:
    for contact in contact_list:
        if contact.get('name') == name:
            return contact


def edit_user():
    choose_contact = input("Напишите контакт который вы хотите изменить\n").capitalize()
    contacted_user = get_contact(contact, choose_contact)

    if contacted_user:
        find_user(choose_contact)
        choose_reset = input("Что вы хотите изменить? Выбор = имя/номер\n").lower()

        if choose_reset == "имя" or choose_reset == "name":
            choose_name = input("Введите новое имя пользователя\n").capitalize()
            if contacted_user and check_numbers(choose_name) and not get_contact(contact, choose_name):
                contacted_user['name'] = choose_name
                return print("Имя изменено!")
            else:
                return print("Пользователь с таким именнем существует")

        elif choose_reset == "номер" or choose_reset == "phone":
            choose = input("\nКакой номер вы хотите изменить? Выбор осуществляется с помощью индексов\n")
            if int(choose) <= len(contacted_user['phone']):
                choose_phone = input("Введите новый номер телефона\n")
                if check_words(choose_phone):
                    index_number = int(choose) - 1
                    contacted_user['phone'][index_number] = choose_phone
                    return print("Номер изменен!")

            else:
                print("Введенный вами номер не существует")

        else:
            print("Неверная команда попробуйте снова")
    else:
        notFound()


def show_number(find):
    number = get_contact(contact, find)
    return number["phone"]


def delete_user():
    delete_name = input("Какого пользователя вы хотите удалить?\n").capitalize()
    user_delete = get_contact(contact, delete_name)
    if user_delete:
        find_user(delete_name)
        if user_delete['name'] and continue_user():
            contact.remove(user_delete)
            return print("Действие завершено")
        else:
            return
    else:
        notFound()


def delete_number():
    user = input("Введите контакт для удаление номер\n").capitalize()
    contacted_user = get_contact(contact, user)
    if contacted_user:
        find_user(user)
        choose_number = input("Какой номер вы хотите удалить? Выбор осуществляется с помощью индексов\n")
        if len(show_number(user)) == 1:
            return print("Действие невозможно, так как у пользователя один номер")
        elif int(choose_number) <= len(contacted_user['phone']) and continue_user():
            choose_number = int(choose_number) - 1
            contacted_user['phone'].pop(choose_number)
            return print("Номер удален!")
    else:
        notFound()


def choose_user():
    choose = input(
        "\n[1] Вывести контакты\n[2] Найти контакт\n[3] Добавить контакт\n[4] Добавить номер для контакта\n[5] Изменить "
        "контакт\n[6] Удалить контакт\n[7] Удалить номер контакта\n[0] Выход\n")
    return choose


def main_menu():
    print("Добро пожаловать в телефонную книгу, Пожалуйста сделайте выбор по индексам ниже")
    while True:
        match choose_user():
            case "1":
                print(contact_number())
            case "2":
                find = input("Пожалуйста напишите имя контакта\n").capitalize()
                find_user(find)
            case "3":
                add_user()
            case "4":
                add_phone()
            case "5":
                edit_user()
            case "6":
                delete_user()
            case "7":
                delete_number()
            case "0":
                if continue_user():
                    break
            case _:
                print("Введеная вами команда не существует. Пожалуйста попробуете снова")

        contact_number()
        write_file(contact)


main_menu()


