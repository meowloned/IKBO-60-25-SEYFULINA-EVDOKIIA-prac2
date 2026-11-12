import sys
from src.config import parse_args
from src.graph import build_graph, build_reverse_graph


def main(argv=None):
    args = parse_args(argv)

    try:
        if args.reverse:
            graph = build_reverse_graph(args)
        else:
            graph = build_graph(args)
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    if not graph:
        print("Пакет исключен фильтром")
        return 0

    if args.reverse:
        print(f"Обратные зависимости {args.reverse}:")
    else:
        print(f"Граф зависимостей {args.package}=={args.version}:")

    for package, dependencies in graph.items():
        text = ", ".join(dependencies) if dependencies else "-"
        print(f"{package}: {text}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())