import argparse
from pathlib import Path
import shutil


def parse_arg():
    parser = argparse.ArgumentParser(description="Копіювання файлів")
    parser.add_argument("-s", "--source", type=Path, required=True, help="Джерело")
    parser.add_argument("-d", "--destination", type=Path, default=Path("output"), help="Куди")
    return parser.parse_args()

def recursive_copy(source: Path, destination: Path):
    for item in source.iterdir():
        # if item.is_dir():
        #     recursive_copy(item, destination)
        # else:
        #     folder = item.name[:1]
        #     folder = destination / folder
        #     folder.mkdir(exist_ok=True, parents=True)
        #     shutil.copy(item, folder)
        if item.is_file():
            folder = item.name[:1]
            folder = destination / folder
            folder.mkdir(exist_ok=True, parents=True)
            shutil.copy(item, folder)
        else:
            recursive_copy(item, destination)

if __name__ == "__main__":
    args = parse_arg()
    recursive_copy(args.source, args.destination)
