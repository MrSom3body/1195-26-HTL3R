__author__ = "Karun Sandhu"

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
        default="WARNING",
    )
    parser.add_argument(
        "-a",
        "--author",
        help="The author to filter the commits for.",
        type=str,
        default="",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="The directory of the git repository.",
        type=str,
        default=".",
    )
    parser.add_argument(
        "-f",
        "--filename",
        help="The filename of the plot.",
        required=True,
        type=str,
    )

    args = parser.parse_args()
