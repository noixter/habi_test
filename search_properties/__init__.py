import configparser
import os.path

config_path = os.path.join(os.path.dirname(__file__), "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

assert "DATABASE" in config.sections(), "database configurations are not set yet"
