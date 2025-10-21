__author__ = "Karun Sandhu"

import argparse
import subprocess
from datetime import datetime

import dateutil


def get_commits(author: str = "", directory: str = ".") -> list[datetime]:
    """
    Get the commit history from a git repository.
    :param author: the author to filter for
    :param directory: the directory of the git repository
    :return: a list of datetime objects of commits
    """
    cmd = [
        "git",
        "-C",
        directory,
        "log",
        "--author",
        author,
        "--pretty=format:%ad",
        "--date=rfc2822",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = result.stdout.strip().split("\n")
    return [dateutil.parser.parse(commit) for commit in commits if commit]


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
