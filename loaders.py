from sshcheckers import ssh_get_value
from datetime import datetime
import paramiko


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Saving file {local_path} to path {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Loading file {local_path} to path {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def time_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_journalctl(name, date_time):
    with open(name, "a") as wf:
        wf.write(ssh_get_value("0.0.0.0", "user2", "2222", "journalctl --since {}".format(date_time)))
