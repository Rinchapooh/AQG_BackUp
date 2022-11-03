import json
import logging
from types import SimpleNamespace


def load_config(filename: str) -> object:
    try:
        with open(filename, 'r') as fb:
            return json.load(fb, object_hook=lambda d: SimpleNamespace(**d))
    except FileNotFoundError as e:
        logging.warning(f'Load config file: {e.strerror}')
        return
    except json.decoder.JSONDecodeError as e:
        logging.warning(f'Parsing config file: {e.msg}')
        return


