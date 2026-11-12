import json
import re
from src.repository import get_dependencies


def normalize_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def validate_test_repository(repository):
    if not isinstance(repository, dict):
        raise ValueError("Тестовый репозиторий должен быть объектом JSON")

    for package, dependencies in repository.items():
        if not re.fullmatch(r"[A-Z]+", package):
            raise ValueError("Имена тестовых пакетов должны состоять из A-Z")

        if not isinstance(dependencies, list):
            raise ValueError(f"Зависимости {package} должны быть списком")

        for dependency in dependencies:
            if not isinstance(dependency, str) or dependency not in repository:
                raise ValueError(f"Не описан пакет: {dependency}")


def load_test_repository(path):
    try:
        with open(path, encoding="utf-8") as file:
            repository = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Ошибка чтения тестового файла: {error}") from error

    validate_test_repository(repository)
    return repository


def package_dependencies(package, root, args, repository):
    if repository is not None:
        return repository[package]

    version = args.version if package == root else None
    requirements = get_dependencies(args.repository, package, version)

    dependencies = []
    for requirement in requirements:
        match = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", requirement.strip())

        if not match:
            raise ValueError(f"Некорректная зависимость: {requirement}")

        name = normalize_name(match.group())
        if name not in dependencies:
            dependencies.append(name)

    return dependencies


def bfs_recursive(level, depth, graph, args, repository, root):
    if not level or depth >= args.max_depth:
        return

    next_level = []

    for package in level:
        dependencies = package_dependencies(package, root, args, repository)

        for dependency in dependencies:
            if args.filter and args.filter.lower() in dependency.lower():
                continue

            if dependency not in graph[package]:
                graph[package].append(dependency)

            if dependency not in graph:
                graph[dependency] = []
                next_level.append(dependency)

    bfs_recursive(next_level, depth + 1, graph, args, repository, root)


def build_graph(args):
    repository = None
    root = normalize_name(args.package)

    if args.test_mode:
        root = args.package
        repository = load_test_repository(args.repository)

        if root not in repository:
            raise ValueError(f"Пакет {root} отсутствует в тестовом репозитории")

    if args.filter and args.filter.lower() in root.lower():
        return {}

    graph = {root: []}
    bfs_recursive([root], 0, graph, args, repository, root)

    return graph


def reverse_repository(repository):
    reversed_repository = {}

    for package in repository:
        reversed_repository[package] = []

    for package, dependencies in repository.items():
        for dependency in dependencies:
            if package not in reversed_repository[dependency]:
                reversed_repository[dependency].append(package)

    return reversed_repository


def build_reverse_graph(args):
    target = args.reverse if args.test_mode else normalize_name(args.reverse)

    if args.filter and args.filter.lower() in target.lower():
        return {}

    if args.test_mode:
        repository = load_test_repository(args.repository)

        if args.package not in repository:
            raise ValueError(f"Пакет {args.package} отсутствует в репозитории")
    else:
        repository = build_graph(args)

    if target not in repository:
        raise ValueError(f"Пакет {target} отсутствует в рассматриваемом графе")

    reversed_repository = reverse_repository(repository)
    graph = {target: []}

    bfs_recursive([target], 0, graph, args, reversed_repository, target)

    return graph