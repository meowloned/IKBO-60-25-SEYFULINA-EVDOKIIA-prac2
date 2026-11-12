import sys

from src.config import parse_args
from src.repository import get_dependencies


def main(argv=None):
    args = parse_args(argv)

    if args.test_mode:
        print("Чтение тестового файла добавим на этапе 3", file=sys.stderr)
        return 1

    try:
        dependencies = get_dependencies(
            args.repository, args.package, args.version
        )
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(f"Прямые зависимости {args.package}=={args.version}:")

    if not dependencies:
        print("Зависимости не указаны")

    for dependency in dependencies:
        print(dependency)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())