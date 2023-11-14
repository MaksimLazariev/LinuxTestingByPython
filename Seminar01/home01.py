# Задание 1.
# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её
# выводе и False в противном случае. Передаваться должна только одна строка, разбиение
# вывода использовать не нужно.


import subprocess


def find_text(command: str, text: str) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="UTF-8")
    if text in result.stdout and result.returncode == 0:
        return True
    return False


if __name__ == '__main__':
    print(find_text("cat /etc/os-release", "22.04.1"))
    print(find_text("cat /etc/os-release", "25.04.1"))

    print(find_text("cat /etc/os-release", "jammy"))
    print(find_text("cat /etc/os-release", "jimmy"))

    print(find_text("cat task01.sh", "$RESULT"))