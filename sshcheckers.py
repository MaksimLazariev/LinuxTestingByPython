import paramiko


def ssh_checkout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()  # инициализация экземпляра метода подключения
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Позв-т авт-ки добавлять все ключи и политики
    client.connect(hostname=host, username=user, password=passwd, port=port)  # Инициализация подкл
    stdin, stdout, stderr = client.exec_command(cmd)  # задание 3х потоков данных
    exit_code = stdout.channel.recv_exit_status()  # Код выхода
    out = (stdout.read() + stderr.read()).decode("utf-8")  # Получ код выхода
    client.close()  # Закрытие поключения
    if text in out and exit_code == 0:  # проверка на вхождение текста в out,  заверш прогр положительно
        return True
    else:
        return False


def ssh_checkout_negative(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()  # инициализация экземпляра метода подключения
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Позв-т авт-ки добавлять все ключи и политики
    client.connect(hostname=host, username=user, password=passwd, port=port)  # Инициализация подкл
    stdin, stdout, stderr = client.exec_command(cmd)  # задание 3х потоков данных
    exit_code = stdout.channel.recv_exit_status()  # Код выхода
    out = (stdout.read() + stderr.read()).decode("utf-8")  # Получ код выхода
    client.close()  # Закрытие поключения
    if text in out and exit_code != 0:  # проверка на вхождение текста в out,  заверш прогр положительно
        return True
    else:
        return False


def ssh_get_value(host, user, passwd, cmd, port=22):
    client = paramiko.SSHClient()  # инициализация экземпляра метода подключения
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Позв-т авт-ки добавлять все ключи и политики
    client.connect(hostname=host, username=user, password=passwd, port=port)  # Инициализация подкл
    stdin, stdout, stderr = client.exec_command(cmd)  # задание 3х потоков данных
    exit_code = stdout.channel.recv_exit_status()  # Код выхода
    out = (stdout.read() + stderr.read()).decode("utf-8")  # Получ код выхода
    client.close()  # Закрытие поключения
    if exit_code == 0:  # проверка на заверш прогр положительно
        return out
    else:
        return False
