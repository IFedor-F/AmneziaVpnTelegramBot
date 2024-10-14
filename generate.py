import ipaddress
import re
import subprocess
import sys

from Config import ConfigList


def fill_pattern(text: str, values: dict[str, str]) -> str:
    pattern = re.compile(r"\$(\w+)")

    def replace_pattern(match):
        key = match.group(1)
        return values.get(key, match.group(0))

    return re.sub(pattern, replace_pattern, text)


def get_next_ip(config_name):
    ip_addresses = [ipaddress.ip_network(ip, strict=False)
                    for ip in ConfigList[config_name].awg_config.get_allowed_ips()]

    if not ip_addresses:
        raise ValueError("No IP addresses configured")
    max_ip = None
    for net in ip_addresses:
        if isinstance(net, ipaddress.IPv4Network) or isinstance(net, ipaddress.IPv6Network):
            ip = list(net.hosts())[0] if net.num_addresses > 1 else net.network_address
        else:
            ip = net.network_address
        if max_ip is None or ip > max_ip:
            max_ip = ip
    return f"{max_ip + 1}/32"


def add_user(config_name, comment):
    if ConfigList[config_name] is None:
        raise KeyError(f"Config {config_name} was not found.")
    next_ip = get_next_ip(config_name)
    private_key, public_key = subprocess.run([sys.executable, 'awg_keygen.py'], stdout=subprocess.PIPE, text=True).stdout.split()
    data = fill_pattern(ConfigList[config_name].user_config_pattern, {"private_key": private_key, "client_local_ip": next_ip})
    ConfigList[config_name].awg_config.append_user(comment, PublicKey=public_key, AllowedIPs=next_ip)
    subprocess.run(ConfigList[config_name].restart_command, shell=True, capture_output=True, text=True)
    return data
