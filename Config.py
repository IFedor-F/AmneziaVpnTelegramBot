import json
import os


class AWGConfig:
    def __init__(self, config_path: str):
        self.config = None
        self.config_path = config_path
        self.parse_conf()

    def parse_conf(self):
        config = []
        current_section = {}

        with open(self.config_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    if current_section:
                        config.append(current_section)
                        current_section = {}
                    current_section["section"] = line[1:-1]
                else:
                    key, value = line.split("=", 1)
                    current_section[key.strip()] = value.strip()

            if current_section:
                config.append(current_section)

        self.config = config

    def get(self):
        self.parse_conf()
        return self.config

    def append_user(self, comment, **keys):
        with open(self.config_path, "a", encoding="UTF-8") as file:
            formatted_keys = '\n'.join(f'{key} = {value}' for key, value in keys.items())
            file.write(f"\n# {comment}\n[Peer]\n{formatted_keys}\n")
        self.parse_conf()

    def get_allowed_ips(self):
        self.parse_conf()
        ips = [peer["AllowedIPs"] for peer in self.config if peer["section"] == "Peer"]
        ips.extend([peer["Address"] for peer in self.config if peer["section"] == "Interface"])
        return ips


class Config:
    def __init__(self, name: str, config: dict):
        self.restart_command: str = config.get("restart_command")
        self.path_to_awg_config: str = config.get("path_to_config")
        self.awg_config: AWGConfig = AWGConfig(self.path_to_awg_config)
        with open(f"user_config_awg_patterns/{name}.pattern", encoding="UTF-8") as file:
            self.user_config_pattern: str = file.read()


class ConfigListMeta(type):
    _configs: dict

    def __getitem__(cls, key) -> Config:
        return cls._configs.get(key, None)


class ConfigList(metaclass=ConfigListMeta):
    with open("config.json") as f:
        config = json.load(f)
    _configs: dict[str, Config] = {name: Config(name, data) for name, data in config.items()}


class TgConfig:
    with open("tg_config.json", "r", encoding="UTF-8") as file:
        config = json.load(file)
    admin_ids: list[int] = config.get("admin_ids")
    API_TOKEN: str = os.getenv(config.get("API_TOKEN_ENV_NAME"))
