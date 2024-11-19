import argparse
from pathlib import Path
import sys
import re


def match_pattern(line: str, pattern: str) -> bool:
    return bool(re.search(pattern, line))


def parse_filename(pattern, filename, print_filename=False):
    with open(filename) as file_:
        found = False
        line = file_.readline()
        while line:
            if match_pattern(line, pattern):
                found = True
                line = f"{filename}:{line}" if print_filename else line
                print(line, end="")
            line = file_.readline()
        return found


def parse(pattern, path_pattern, recursive):
    if path_pattern == "*":
        path_pattern = "."
    path = Path(path_pattern)
    if not path.exists():
        print(f"{path}: No such file or directory")
        sys.exit(1)
    if path.is_dir() and not recursive:
        print(f"{path}: Is a directory")
        sys.exit(1)
    if path.is_file():
        return parse_filename(pattern, path)
    found = False
    for file_path in path.rglob("*.txt"):
        if parse_filename(pattern, file_path, print_filename=True):
            found = True
    return found


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="grep",
        description="Simple grep implementation written in Python"
    )
    parser.add_argument("pattern")
    parser.add_argument("filename")
    parser.add_argument("-r", "--recursive", action="store_true")
    args = parser.parse_args()
    found = parse(args.pattern, args.filename, args.recursive)
    if not found:
        sys.exit(1)