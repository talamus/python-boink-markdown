import os
import sys
import pathlib
import datetime
from enum import Enum
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from .configuration import getConfiguration
from colorama import Fore, Style
import pprint
import textwrap


VERBOSITY = {
    "NONE": None,
    "ERROR": logging.ERROR,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


class ScreenFormatter(jsonlogger.JsonFormatter):
    """A screen friendly version of the log record."""

    VERBOSITY_COLORS = {
        "ERROR": Style.BRIGHT + Fore.RED,
        "INFO": Style.BRIGHT + Fore.GREEN,
        "DEBUG": Style.BRIGHT + Fore.YELLOW,
    }

    def format_extra_field(self, name, value):
        title = f"{name}: "
        content = textwrap.indent(
            pprint.pformat(value, sort_dicts=False), len(title) * " "
        ).strip()
        combined = textwrap.indent(f"{title}{content}", 4 * " ")
        return f"\n{combined}"

    def jsonify_log_record(self, log_record):
        log_record.pop("asctime")  # Timestamp (skipped)
        log_record.pop("name")  # Name of the logger (skiped)
        levelname = log_record.pop("levelname")  # Logging level (color)
        message = log_record.pop("message")  # Actual message
        extra_fields = []
        for key, value in log_record.items():
            extra_fields.append(self.format_extra_field(key, value))
        extra_fields = "\n" + "\n".join(extra_fields) + "\n" if extra_fields else ""
        return f"{self.VERBOSITY_COLORS[levelname]}{message}{Style.RESET_ALL}{extra_fields}"


class LogFileFormatter(jsonlogger.JsonFormatter):
    """A log file friendly version of the log record."""

    def add_fields(self, log_record, record, message_dict):
        """Format a timestamp and a level information."""
        super(LogFileFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.datetime.utcfromtimestamp(
                record.created
            ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def setupLoggers() -> None:
    cfg = getConfiguration()

    # We are configuring the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # Screen output (a.k.a Verbosity/Quiet)
    if cfg.verbosity and VERBOSITY[cfg.verbosity]:
        handler = logging.StreamHandler(sys.stdout)
        formatter = ScreenFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(VERBOSITY[cfg.verbosity])
        logger.addHandler(handler)

    # Logging to a log file
    if cfg.log_level and cfg.log_file:
        # Try to create the log dir
        log_dir, _ = os.path.split(cfg.log_file)
        pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)

        # Rotate logs either by time:
        if "log_when_to_rotate" in cfg:
            handler = logging.handlers.TimedRotatingFileHandler(
                cfg.log_file,
                when=cfg.log_when_to_rotate,
                backupCount=cfg.log_max_files,
            )

        # Or by file size
        else:
            handler = logging.handlers.RotatingFileHandler(
                cfg.log_file,
                maxBytes=cfg.log_max_bytes,
                backupCount=cfg.log_max_files,
            )

        formatter = LogFileFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(VERBOSITY[cfg.log_level])
        logger.addHandler(handler)
