import yaml
from checkers import get_value
from sshcheckers import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step01(self, make_folders, clear_folders, make_files):
        # test01, archive arx2.xx created
        result01 = ssh_checkout("0.0.0.0", "user2", "2222",
                                "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data["type"], data["folder_out"]),
                                'Everything is Ok')
        result02 = ssh_checkout("0.0.0.0", "user2", "2222", "ls {}".format(data["folder_out"]), "arx2")
        assert result01 and result02, "test01 Failed"

    def test_step02(self, clear_folders, make_files):
        # test02 extracting files from archive arx.7z to folder01 by 'e'
        result_list = []
        result_list.append(
            ssh_checkout("0.0.0.0", "user2", "2222",
                         "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data["type"], data["folder_out"]),
                         'Everything is Ok'))
        result_list.append(ssh_checkout("0.0.0.0", "user2", "2222",
                                        "cd {}; 7z e -t{} arx2.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                                  data["type"], data["folder_ext01"]),
                                        "Everything is Ok"))
        for item in make_files:
            result_list.append(ssh_checkout("0.0.0.0", "user2", "2222", "ls {}".format(data["folder_ext01"]), item))
        assert all(result_list), "test02 Failed"

    def test_step03(self):
        # test03 checking archive totality
        assert ssh_checkout("0.0.0.0", "user2", "2222",
                            "cd {}; 7z t -t{} arx2.{}".format(data["folder_out"], data["type"], data["type"]),
                            "Everything is Ok"), "test03 FAIL"

    def test_step04(self):
        # test04 updating arx2.7z for new files
        assert ssh_checkout("0.0.0.0", "user2", "2222",
                            "cd {}; 7z u -t{} {}/arx2.{}".format(data["folder_ext01"], data["type"], data["folder_out"],
                                                                 data["type"]), "Everything is Ok"), "test04 FAIL"

    def test_step05(self, clear_folders, make_files):
        # test05 checking list of files in archive arx.7z
        result_list = []
        result_list.append(ssh_checkout("0.0.0.0", "user2", "2222",
                                        "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data["type"],
                                                                          data["folder_out"]), 'Everything is Ok'))
        for item in make_files:
            result_list.append(ssh_checkout("0.0.0.0", "user2", "2222",
                                            "cd {}; 7z l -t{} arx2.{}".format(data["folder_out"], data["type"],
                                                                              data["type"]), item))
        assert all(result_list), "test05 FAIL"

    def test_step06(self, clear_folders, make_files, make_subfolder):
        # test06 extracting files from archive arx.7z to folder02 by 'x'
        result_list = []
        result_list.append(ssh_checkout("0.0.0.0", "user2", "2222",
                                        "cd {}; 7z a -t{} {}/arx".format(data["folder_in"], data["type"],
                                                                         data["folder_out"]), 'Everything is Ok'))
        result_list.append(ssh_checkout("0.0.0.0", "user2", "2222",
                                        "cd {}; 7z x -t{} arx.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                                 data["type"], data["folder_ext02"]),
                                        "Everything is Ok"))

        for item in make_files:
            result_list.append(ssh_checkout("0.0.0.0", "user2", "2222", "ls {}".format(data["folder_ext02)"], item)))

        result_list.append(
            ssh_checkout("0.0.0.0", "user2", "2222", "ls {}".format(data["folder_ext02"]), make_subfolder[0]))
        result_list.append(
            ssh_checkout("0.0.0.0", "user2", "2222", "ls {}/{}".format(data["folder_ext02"], make_subfolder[0]),
                         make_subfolder[1]))
        assert all(result_list), "test06 Failed"

    def test_step07(self):
        # test07 files in archive arx.7z deleted
        assert ssh_checkout("0.0.0.0", "user2", "2222",
                            "cd {}; 7z d -t{} arx.{}".format(data["folder_out"], data["type"], data["type"]),
                            "Everything is Ok"), "test07 FAIL"

    def test_step08(self, clear_folders, make_files, deploy_css32):
        # test08 checking hash of files in folder_in folder by 'h' and 'crc32'
        result_list = []
        for item in make_files:
            result_list.append(
                ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z h {}".format(data["folder_in"], item),
                             'Everything is Ok'))
            crc32_hash = get_value("cd {}; crc32 {}".format(data["folder_in"], item))
            result_list.append(
                ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z h {}".format(data["folder_in"], item),
                             crc32_hash.upper()))
        assert all(result_list), "test08 Failed"
