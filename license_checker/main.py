from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from loguru import logger  # type: ignore


def license_in_file(file_path: str | Path) -> bool:
    license = 'License='
    with open(file_path) as file:
        content = file.read()
    return (license in content) \
        or (license.upper() in content) \
        or (license.lower() in content)


def files_have_the_license(files_path: Sequence[str | Path]) -> bool:
    files_status = []
    for index, file in enumerate(files_path):
        logger.info(f"checking {index + 1}/{len(files_path)}: {file}...")
        status = license_in_file(file)
        files_status.append(status)
        if status:
            logger.error(f"{file} contains license ❌")
        else:
            logger.success(f"{file} doesn't contain license ✅")

    return any(files_status)


def license_checker(files: Sequence[str | Path]) -> int:
    if files_have_the_license(files):
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--files', nargs='*',
        help='files in which the license will be checked',
    )
    args = parser.parse_args(argv)

    if not args.files:
        raise ValueError(
            'You must provide some file paths to check if they contain a '
            'license. E.g.: --files README.md some_package/__init__.py',
        )

    return license_checker(args.files)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
