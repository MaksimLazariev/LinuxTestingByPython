import pytest
from checkers import checkout, get_value
from datetime import datetime
import random
import string
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(
        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext01"], data["folder_ext02"]),
        "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext01"],
                                                        data["folder_ext02"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if /dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                           filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
                                                                                      testfilename, data["bs"]), ""):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("End: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a -t{} {}/bad_arx.{}".format(data["folder_in"], data["type"], data["folder_out"], data["type"]),
             "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True, scope="class")
# make file one time
def make_stat_file():
    with open(data["stat_file"], "w") as wf:
        wf.write('Test Statistics\n')


@pytest.fixture(autouse=True, scope="function")
# add stats in file after each test running
def put_stat_data():
    yield
    with open(data["stat_file"], "a") as wf:
        wf.write('Time={}, Num of files={}, File size={}, Cpu stats={}\n'.format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                                 data["count"], data["bs"],
                                                                                 get_value("cat /proc/loadavg")[:-1]))
