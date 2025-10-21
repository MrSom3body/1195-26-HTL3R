__author__ = "Karun Sandhu"

import argparse
import subprocess
from collections import Counter
from datetime import datetime, timedelta

import dateutil
import matplotlib.pyplot as plt


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
        "--all",
        "--author",
        author,
        "--pretty=format:%ad",
        "--date=rfc2822",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = result.stdout.strip().split("\n")
    return [dateutil.parser.parse(commit) for commit in commits if commit]


def generate_git_graph(author: str, commits: list[datetime], filename: str) -> None:
    """
    Generate a git graph (scatter plot) from a list of commits, which displays the last seven weekdays on the y-axis and the time (0-23) on the x-axis.
    :param commits: a list of datetime objects of commits
    :param filename: the filename of the plot
    """
    if not commits:
        print("No commits found — nothing to plot.")
        return

    now = datetime.now(dateutil.tz.tzlocal())
    week_ago = now - timedelta(days=7)
    commits = [c for c in commits if week_ago <= c <= now]

    if not commits:
        print("No commits in the last 7 days.")
        return

    commit_counts = Counter((c.weekday(), c.hour) for c in commits)

    today = now.weekday()  # Monday=0 ... Sunday=6
    weekday_order = [(today - i) % 7 for i in range(6, -1, -1)]
    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekday_labels = [weekday_labels[w] for w in weekday_order]

    hours = []
    weekdays = []
    sizes = []
    for (w, h), count in commit_counts.items():
        new_y = weekday_order.index(w)
        weekdays.append(new_y)
        hours.append(h)
        sizes.append(count * 100)

    title = (
        f"Git Commits by {author}: {len(commits)} (last 7 days)"
        if author
        else f"Git Commits: {len(commits)} (last 7 days)"
    )
    plt.title(title)

    plt.scatter(hours, weekdays, s=sizes, alpha=0.4)

    ax = plt.gca()
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Weekday")
    ax.set_aspect(24 / 7)

    plt.xticks(range(0, 24, 2), [str(t) for t in range(0, 24, 2)])
    plt.yticks(range(7), weekday_labels)

    plt.tight_layout()
    # padding
    ax.set_xlim(-1, 24)
    ax.set_ylim(-0.5, 6.5)
    plt.savefig(filename, dpi=150)
    plt.close()


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

    commits = get_commits(author=args.author, directory=args.directory)
    generate_git_graph(author=args.author, commits=commits, filename=args.filename)
