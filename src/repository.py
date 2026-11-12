import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

TIMEOUT = 10
NOT_FOUND = 404


def extract_dependencies(data):
    if not isinstance(data, dict) or not isinstance(data.get("info"), dict):
        raise ValueError("В ответе репозитория нет сведений о пакете")

    dependencies = data["info"].get("requires_dist")

    if dependencies is None:
        return []

    if not isinstance(dependencies, list):
        raise ValueError("Некорректный список зависимостей")

    for dependency in dependencies:
        if not isinstance(dependency, str):
            raise ValueError("Зависимость должна быть строкой")

    return dependencies


def get_dependencies(repository, package, version):
    url = f"{repository.rstrip('/')}/{package}"

    if version is not None:
        url += f"/{version}"

    url += "/json"
    
    try:
        with urlopen(url, timeout=TIMEOUT) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code == NOT_FOUND:
            raise ValueError("Пакет или версия не найдены") from error

        message = f"Репозиторий вернул ошибку HTTP {error.code}"
        raise ValueError(message) from error
    except (URLError, TimeoutError) as error:
        raise ValueError(f"Ошибка соединения: {error}") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("Репозиторий вернул некорректный JSON") from error

    return extract_dependencies(data)