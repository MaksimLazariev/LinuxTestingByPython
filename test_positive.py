import subprocess

tst = "/home/user/tst"  # 'tst' contains file 'qwe' and folder 'tst_fldr', 'tst_fldr' contains 'sty'
out = "/home/user/out"  # contains arx2.7z
folder01 = "/home/user/folder01"    # contains unpacked files by 'e' command
folder02 = "/home/user/folder02"    # contains unpacked files by 'x' command
tst_fldr = "/home/user/folder02/tst_fldr"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def get_value(cmd):     # get str value by command
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


def test_step01():
    # test01, archive arx2.7z created
    result01 = checkout("cd {}; 7z a {}/arx2".format(tst, out), 'Everything is Ok')
    result02 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result01 and result02, "test01 Failed"


def test_step02():
    # test02 extracting files from archive arx.7z to folder01 by 'e'
    result01 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder01), "Everything is Ok")
    result02 = checkout("cd {}; ls".format(folder01), "qwe")
    result03 = checkout("cd {}; ls".format(folder01), "rty")
    assert result01 and result02 and result03, "test02 Failed"


def test_step025():
    # test02.5 checking list of files in archive arx.7z
    result01 = checkout("cd {}; 7z l arx2.7z".format(out), "qwe")
    result02 = checkout("cd {}; 7z l arx2.7z".format(out), "rty")
    assert result01 and result02, "test02.5 FAIL"


def test_step026():
    # test02.6 extracting files from archive arx.7z to folder02 by 'x'
    result01 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(out, folder02), "Everything is Ok")
    result02 = checkout("cd {}; ls".format(folder02), "qwe")
    result03 = checkout("cd {}; ls".format(tst_fldr), "rty")
    assert result01 and result02 and result03, "test02.6 Failed"


def test_step027():
    # test02.7 checking hash of archive arx.7z by 'h' and 'crc32'
    crc32_hash = get_value("cd {}; crc32 arx2.7z".format(out))     # get hash value of archive by 'crc32' command
    result01 = checkout("cd {}; 7z h arx2.7z".format(out), crc32_hash.upper())  # compare hash values by 'h' and 'crc32' commands
    assert result01, "test02.7 Failed"


def test_step03():
    # test03 checking archive totality
    assert checkout("cd {}; 7z t arx2.7z".format(out), "Everything is Ok"), "test03 FAIL"


def test_step04():
    # test04 updating arx2.7z for new files
    assert checkout("cd {}; 7z u {}/arx2".format(tst, out), "Everything is Ok"), "test04 FAIL"


def test_step05():
    # test05 files in archive arc2.7z deleted
    assert checkout("cd {}; 7z d  arx2.7z".format(out), "Everything is Ok"), "test05 FAIL"




