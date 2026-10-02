import socket
import ftplib
import paramiko
import tempfile
import subprocess
import time
import os

# Credenciais para tentativa
DEFAULT_USERS = ['admin', 'user', 'root', 'guest', 'test', 'ftp', 'web']
DEFAULT_PASSWORDS = ['admin', '123456', 'password', 'root', 'guest', '12345', '1234']

SERVICES = {
    'http': 80, 'ssh': 22, 'ftp': 21,
    'telnet': 23, 'smb': 445, 'mysql': 3306,
    'rdp': 3389, 'vnc': 5900,
}


def is_port_open(ip: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def check_ssh(ip: str, port: int) -> tuple[bool, str]:
    for user in DEFAULT_USERS:
        for pwd in DEFAULT_PASSWORDS:
            try:
                c = paramiko.SSHClient()
                c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                c.connect(ip, port=port, username=user, password=pwd, timeout=2)
                c.close()
                return True, f"{user}:{pwd}"
            except Exception:
                pass
    return False, ""


def check_ftp(ip: str, port: int) -> tuple[bool, str]:
    for user in DEFAULT_USERS:
        for pwd in DEFAULT_PASSWORDS:
            try:
                ftp = ftplib.FTP()
                ftp.connect(ip, port, timeout=2)
                ftp.login(user, pwd)
                ftp.quit()
                return True, f"{user}:{pwd}"
            except Exception:
                pass
    return False, ""
