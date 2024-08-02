import argparse
import json
import logging


def setup_logger(args):
    if args.debug:
        logging.basicConfig(level=logging.info, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_args(sysargs):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode.",
    )

    args = parser.parse_args(sysargs)
    return args


def get_pushover_keys(file_path):
    with open(file_path, 'r') as file:
        # Parse the JSON data
        data = json.load(file)
    return (data["token"], data["user"])
