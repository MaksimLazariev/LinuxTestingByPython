import pytest
from sshcheckers import ssh_checkout, ssh_get_value
from loaders import upload_files, time_now
import random
import string
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext01"],
                                                   data["folder_ext02"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext01"],
                                                            data["folder_ext02"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}; dd if /dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename, data["bs"]),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                                  subfoldername,
                                                                                                  testfilename,
                                                                                                  data["bs"]), ""):
        return subfoldername, None
    return subfoldername, testfilename



@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "2222",
                 "cd {}; 7z a -t{} {}/bad_arx.{}".format(data["folder_in"], data["type"], data["folder_out"],
                                                         data["type"]), "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "2222", "truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True, scope="class")
# make local file
def make_stat_file():
    with open("/home/user/{}".format(data["stat_file"]), "w") as wf:
        wf.write('Test Statistics\n')


@pytest.fixture(autouse=True, scope="function")
# add stats in local file after each test running
def put_stat_data():
    time = time_now()
    yield
    # После выполнения теста собираем статистику cpu и журнал
    cpu_stats = ssh_get_value("0.0.0.0", "user2", "2222", "cat /proc/loadavg")[:-1]
    journal = ssh_get_value("0.0.0.0", "user2", "2222", "journalctl --since '{}'".format(time_now()))
    # Пишем всю информацию в локальный файл статистики
    with open("/home/user/{}".format(data["stat_file"]), "a") as wf:
        wf.write('Time={}, Num of files={}, File size={}, Cpu stats={}\nLog journal:\n{}\n'.format(time,
                                                                                 data["count"], data["bs"],
                                                                                 cpu_stats, journal))


@pytest.fixture(autouse=True, scope="module")
# По завершению всех тестов копируем файл статистики на удаленный компьютер
def upload_stat_data():
    yield
    upload_files("0.0.0.0", "user2", "2222", "/home/user/{}".format(data["stat_file"]), "/home/user2/{}".format(data["stat_file"]))


@pytest.fixture(autouse=True, scope="module")
def deploy_7zip():
    result = []
    upload_files("0.0.0.0", "user2", "2222", "/home/user/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    result.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -i home/user2/p7zip-full.deb",
                               "Настраивается пакет"))
    result.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -s p7zip-full",
                               "Status: install ok installed"))
    return all(result)


@pytest.fixture(autouse=True, scope="module")
def deploy_css32():
    # Установка css32. Аналогична установке 7Zip. Только не переносим файл, пакет уже есть в Python.
    result = []
    result.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo apt install libarchive-zip-perl",
                               "Настраивается пакет"))
    result.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -s libarchive-zip-perl",
                               "Status: install ok installed"))
    return all(result)
