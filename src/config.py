import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit

MAX_DEPTH = 100
PACKAGE_PATTERN = r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?"
VERSION_PATTERN = r"v?[0-9][A-Za-z0-9.!+_-]*"


def package_name(value):
    if not re.fullmatch(PACKAGE_PATTERN, value):
        raise argparse.ArgumentTypeError("некорректное имя пакета")
    return value


def version_string(value):
    if not re.fullmatch(VERSION_PATTERN, value):
        raise argparse.ArgumentTypeError("некорректная версия пакета")
    return value


def depth_value(value):
    try:
        depth = int(value)
    except ValueError as error:
        message = "глубина должна быть целой"
        raise argparse.ArgumentTypeError(message) from error

    if not 0 <= depth <= MAX_DEPTH:
        message = f"глубина должна быть от 0 до {MAX_DEPTH}"
        raise argparse.ArgumentTypeError(message)

    return depth


def filter_string(value):
    if value and (value.isspace() or not value.isprintable()):
        message = "фильтр содержит недопустимые символы"
        raise argparse.ArgumentTypeError(message)
    return value


def build_parser():
    parser = argparse.ArgumentParser(description="Граф зависимостей Python-пакетов.")
    parser.add_argument("--package", required=True, type=package_name)
    parser.add_argument("--version", required=True, type=version_string)
    parser.add_argument("--repository", default="https://pypi.org/pypi")
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--max-depth", type=depth_value, default=3)
    parser.add_argument("--filter", type=filter_string, default="")
    parser.add_argument("--reverse", type=package_name)
    return parser


def validate_url(parser, value):
    try:
        url = urlsplit(value)
        url.port
    except ValueError:
        parser.error("некорректный URL репозитория")

    if url.scheme not in {"http", "https"} or not url.hostname:
        parser.error("репозиторий должен иметь HTTP(S) URL")


def validate_repository(parser, args):
    if args.test_mode:
        if not re.fullmatch(r"[A-Z]+", args.package):
            parser.error("в тестовом режиме имя состоит из букв A-Z")
        if args.reverse and not re.fullmatch(r"[A-Z]+", args.reverse):
            parser.error("имя для --reverse должно состоять из букв A-Z")
        if not Path(args.repository).is_file():
            parser.error("файл тестового репозитория не найден")
        return

    validate_url(parser, args.repository)


def parse_args(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_repository(parser, args)
    return args