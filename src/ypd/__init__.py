from configparser import ConfigParser

relative_path = __file__.rpartition("/")[0]

config = ConfigParser()
config.read(f'{relative_path}/config/config.ini')