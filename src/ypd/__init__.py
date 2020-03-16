from configparser import ConfigParser
from pathlib import Path

relative_path = str(Path(__file__).parent)
config = ConfigParser()
config.read(f'{relative_path}/config/config.ini')
