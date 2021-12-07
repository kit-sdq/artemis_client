import configparser
import os
import logging

CONFIG_FILE = os.getenv("ARTEMIS_CLIENT_CONFIG", "config.ini")
PARSER = None

if PARSER is None:
    if os.path.isfile(CONFIG_FILE):
        PARSER = configparser.ConfigParser()
        PARSER.read(CONFIG_FILE)

def get_value(section: str, key:str) -> str:
    environ_key = f"{section}_{key}"
    if environ_key in os.environ:
        return os.environ[environ_key]
    else:
        logging.debug(f"{environ_key} was not found in environment variables.")

    if PARSER and section in PARSER and key in PARSER[section]:
        return PARSER[section][key]

    raise KeyError(f"""Configuration option for ({section}, {key}) was not found.
                   Please provide a file {CONFIG_FILE} with the section {section} and a key {key}
                   or a environment variable {environ_key}.
                   """)

