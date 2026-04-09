import json
import os


class ConfigError(Exception):
    pass


def load_config():
    rc_path = os.path.join(os.getcwd(), ".glossaryrc")
    if not os.path.exists(rc_path):
        raise ConfigError(".glossaryrc not found. Run 'glossary.py init' first.")
    with open(rc_path) as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f".glossaryrc is not valid JSON: {e}") from e
    if not {"json_path", "markdown_path"}.issubset(config):
        raise ConfigError(".glossaryrc must contain 'json_path' and 'markdown_path' keys.")
    return config


def write_config(json_path, markdown_path):
    rc_path = os.path.join(os.getcwd(), ".glossaryrc")
    config = {"json_path": json_path, "markdown_path": markdown_path}
    try:
        with open(rc_path, "x") as f:
            json.dump(config, f, indent=2)
            f.write("\n")
    except FileExistsError:
        raise ConfigError(".glossaryrc already exists in this directory.")
