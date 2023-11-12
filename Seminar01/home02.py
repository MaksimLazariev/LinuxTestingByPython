# Задание 2. (повышенной сложности)
# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился
# дополнительный режим работы, в котором вывод разбивается на слова с удалением
# всех знаков пунктуации (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.

import subprocess
import string


def find_text(command: str, text: str, cut_mode: bool = False) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="UTF-8")
    if cut_mode:
        out = cut_punctuation(result.stdout)
    else:
        out = result.stdout
    print(out)  # print added for task control
    if text in out and result.returncode == 0:
        return True
    return False


def cut_punctuation(input_string: str) -> str:
    return input_string.translate(str.maketrans('', '', string.punctuation))


if __name__ == '__main__':
    print(find_text("cat /etc/os-release", "22.04.1", True))
    print(find_text("cat /etc/os-release", "25.04.1", False))
