import re
import subprocess
import sys

from Config import Config

local_ip_pattern = re.compile(r"192\.168\.12\.(?P<n>\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)/32")


def fill_pattern(text: str, values: dict[str, str]) -> str:
    pattern = re.compile(r"\$(\w+)")

    def replace_pattern(match):
        key = match.group(1)
        return values.get(key, match.group(0))

    return re.sub(pattern, replace_pattern, text)


def get_next_ip() -> str:
    ip_list = map(lambda i: re.match(local_ip_pattern, i), Config.awg_config.get_allowed_ips())
    ip_list = map(lambda i: int(i.group('n')), filter(lambda i: i, ip_list))
    next_ip = max(ip_list) + 1
    if next_ip > 255:
        raise AttributeError("Max limit Ip")
    return f"192.168.12.{next_ip}/32"


def add_user(comment):
    next_ip = get_next_ip()
    private_key, public_key = subprocess.run([sys.executable, 'wg_keygen.py'], stdout=subprocess.PIPE, text=True).stdout.split("\n")
    data = fill_pattern(Config.user_config_pattern, {"private_key": private_key, "client_local_ip":next_ip})
    Config.awg_config.append_user(comment, PublicKey=public_key, AllowedIPs=next_ip)
    return data