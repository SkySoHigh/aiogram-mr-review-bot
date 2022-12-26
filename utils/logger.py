import json
import logging
import logging.config


def setup_logging(logging_cfg_path: str):
    try:
        with open(logging_cfg_path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e
