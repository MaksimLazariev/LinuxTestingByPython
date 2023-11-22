import yaml
from sshcheckers import ssh_checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step01(self, make_folders, clear_folders, make_bad_arx):
        # test01
        assert ssh_checkout_negative("0.0.0.0", "user2", "2222",
                                     "cd {}; 7z e -t{} bad_arx.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                                  data["type"],
                                                                                  ["folder_ext01"]),
                                     "ERRORS"), "test01 Failed"

    def test_step02(self, make_folders, clear_folders, make_bad_arx):
        # test02
        assert ssh_checkout_negative("0.0.0.0", "user2", "2222",
                                     "cd {}; 7z t -t{} bad_arx.{}".format(data["folder_out"], data["type"],
                                                                          data["type"]),
                                     "ERRORS"), "test02 FAIL"
