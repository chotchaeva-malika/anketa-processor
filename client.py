import requests

BASE_URL = "http://127.0.0.1:5000"


class ServerNedostupen(Exception):
    pass


def _request(method, path, **kwargs):
    try:
        response = requests.request(method, BASE_URL + path, timeout=3, **kwargs)
    except requests.exceptions.ConnectionError:
        raise ServerNedostupen("сервер не отвечает — проверьте, запущен ли server.py")
    except requests.exceptions.Timeout:
        raise ServerNedostupen("превышено время ожидания ответа от сервера (3 сек)")

    if response.status_code >= 500:
        raise ServerNedostupen(f"внутренняя ошибка сервера (код {response.status_code})")

    return response


def get_anketi():
    response = _request("GET", "/anketi")
    if response.status_code == 200:
        return response.json()
    raise ServerNedostupen(f"неожиданный код ответа при получении анкет: {response.status_code}")


def get_anketa(number):
    response = _request("GET", f"/anketi/{number}")
    if response.status_code == 200:
        return response.json()
    if response.status_code == 404:
        return None
    raise ServerNedostupen(f"неожиданный код ответа для анкеты {number}: {response.status_code}")


def check_mail(mail):
    response = _request("POST", "/proverka", json={"mail": mail})
    data = response.json()
    return bool(data.get("prinyato", False))


def get_statistics():
    response = _request("GET", "/statistika")
    if response.status_code == 200:
        return response.json()
    raise ServerNedostupen(f"неожиданный код ответа при получении статистики: {response.status_code}")
