import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config.yaml"


def config_get(path) -> dict:
    with open(path) as filestream:
        parsed_config = yaml.safe_load(filestream)
        return parsed_config


config = config_get(config_path)
