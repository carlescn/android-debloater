import json
import logging
import logging.config
import subprocess

from src.logging import custom_levels


def load_config() -> None:
    config_file = "src/logging/config.json"

    with open(file=config_file, mode="r", encoding="utf-8") as file:
        config = json.load(file)

    logging.addLevelName(custom_levels.STDOUT, "STDOUT")
    logging.config.dictConfig(config)


def subprocess_with_logging(cmd: list[str], logger: logging.Logger = None) -> list[str]:
    logger = logging.getLogger(__name__) if logger is None else logger

    stdout = []
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            stdout.append(line.strip())
            logger.log(custom_levels.STDOUT, line.strip())
        for line in proc.stderr:
            logger.error(line.strip())

    return stdout
