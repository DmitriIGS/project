import configparser


def get_config(section: str, parameter: str) -> str:
    config = configparser.ConfigParser()
    config.read("pytest.ini")
    return config[section][parameter]