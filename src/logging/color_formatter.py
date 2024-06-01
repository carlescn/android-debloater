import logging
from typing import Literal

from src.logging import custom_levels


class ColorFormatter(logging.Formatter):

    grey     = "\033[90m"
    blue     = "\033[34m"
    white    = "\033[97m"
    yellow   = "\033[93m"
    red      = "\033[91m"
    red_bold = "\033[91;1m"
    reset    = "\033[0m"

    def __init__(self, fmt: str, datefmt: str, style: Literal['%', '{', '$']):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.datefmt = datefmt
        self.fmt = "{color:s}" + fmt + self.reset
        self.level_colors = {
            custom_levels.STDOUT: self.blue,
            logging.DEBUG       : self.grey,
            logging.INFO        : self.white,
            logging.WARNING     : self.yellow,
            logging.ERROR       : self.red,
            logging.CRITICAL    : self.red_bold,
        }

    def format(self, record: logging.LogRecord) -> str:
        color = self.level_colors.get(record.levelno, self.white)
        fmt = self.fmt.format(color=color)
        formatter = logging.Formatter(fmt=fmt, datefmt=self.datefmt)
        return formatter.format(record)
