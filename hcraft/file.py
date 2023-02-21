import csv
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Union

import yaml


@contextmanager
def read_or_create_yml(
    path: str | Path,
    encoding: str = "utf-8",
    newline: str | None = None,
    default: Any = "",
    **kwargs
):
    """Open a file if exists; else create a new one with given name"""
    filepath = Path(path)
    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.touch()
        if default:
            write_yml(filepath, default)

    file = open(filepath, mode="r", encoding=encoding, newline=newline, **kwargs)
    try:
        yield yaml.safe_load(file)
    finally:
        file.close()


@contextmanager
def read_yml(
    path: str | Path, encoding: str = "utf-8", newline: str | None = None, **kwargs
):
    file = open(path, mode="r", encoding=encoding, newline=newline, **kwargs)
    try:
        yield yaml.safe_load(file)
    finally:
        file.close()


def write_yml(
    path: str | Path,
    data: Any,
    encoding: str = "utf-8",
    newline: str | None = None,
    **kwargs
):
    with open(path, "w", encoding=encoding, newline=newline, **kwargs) as file:
        yaml.safe_dump(
            data, file, encoding=encoding, allow_unicode=True, sort_keys=False
        )


def yaml2csv(origin_path: str | Path, target_path: str | Path):
    with read_yml(origin_path) as data:
        with open(target_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
