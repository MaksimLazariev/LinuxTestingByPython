import subprocess

out = "/home/user/out"
folder01 = "/home/user/folder01"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step01():
    # test01
    assert checkout("cd {}; 7z e bad_arx.7z -o{} -y".format(out, folder01), "ERRORS"), "test01 Failed"

def test_step02():
    # test02
    assert checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "test02 FAIL"
