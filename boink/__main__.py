import sys
import argparse
import os.path
import yaml
import textwrap
import platformdirs
from .setup import *
import logging

APP_NAME = "boink"
APP_DESCRIPTION = "Git and Markdown Powered Minimalistic CMS"
APP_CONFIG = {
    "config_file": os.path.join(
        platformdirs.user_config_dir(APP_NAME), f"{APP_NAME}.config"
    ),
    "verbosity": "ERROR",
    "log_file": os.path.join(platformdirs.user_log_dir(APP_NAME), f"{APP_NAME}.log"),
    "log_level": "INFO",
    "log_max_bytes": 100 * 1024,
    "log_max_files": 10,
}
APP_USAGE = f"""
Here will be an example...
"""


def _parse_args() -> dict:
    """Parse command line arguments"""

    argparser = argparse.ArgumentParser(
        prog=f"python -m {APP_NAME}",
        description=APP_DESCRIPTION,
        epilog=APP_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    argparser.add_argument(
        "content_paths",
        metavar="content",
        nargs="*",
        help="content to be processed (directory or a markdown file)",
    )
    argparser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="set output verbosity (-v = INFO, -vv = DEBUG)",
    )
    argparser.add_argument(
        "-q",
        "--quiet",
        dest="verbosity",
        action="store_const",
        const=-1,
        help="Do not output anything",
    )
    argparser.add_argument(
        "--config",
        dest="alterative_config_file",
        metavar="CONFIG",
        help="read configuration from this file (YAML format)",
    )
    argparser.add_argument(
        "--loglevel",
        dest="log_level",
        metavar="LEVEL",
        choices=VERBOSITY.keys(),
        default=APP_CONFIG["log_level"],
        help=f"set logging level ({', '.join(list(VERBOSITY.keys()))})",
    )
    argparser.add_argument(
        "--dryrun",
        action="store_true",
        help="do not do anything",
    )
    return argparser.parse_args()


def main() -> None:
    """CLI program."""
    args = _parse_args()

    # Make sure that verbosity is within range and convert it into a string
    verbosity_names = tuple(VERBOSITY.keys())
    args.verbosity = verbosity_names[
        len(verbosity_names) - 1
        if args.verbosity + 2 > len(verbosity_names)
        else args.verbosity + 1
    ]

    # If an alternative configuration file is provided, use it instead of the standard one
    if args.alterative_config_file:
        args.config_file = args.alterative_config_file
    delattr(args, "alterative_config_file")

    # Set up application settings and loggers
    setupConfiguration(APP_CONFIG, vars(args))
    setupLoggers()
    cfg = getConfiguration()

    logger = logging.getLogger(APP_NAME)

    # Run the application
    logger.info(f"Starting {APP_NAME}...")
    logger.debug("Command line arguments:", extra={"argv": sys.argv, "cfg": cfg})
    logger.debug("Combined configuration:", extra={"cfg": cfg})

    # Bye bye!
    logger.info("All Ok!")
    sys.exit(0)


if __name__ == "__main__":
    main()
