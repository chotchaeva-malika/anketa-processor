import requests

BASE = "http://127.0.0.1:5000"


def task_h1():
    print("=== Задача H1. Первый запрос ===")
    r = requests.get(BASE + "/", timeout=3)
    print("Код ответа:", r.status_code)
    print("Тип r.text:", type(r.text))
    print("Тип r.json():", type(r.json()))
    data = r.json()
    print("Ответ сервера:", data)
    for key in ("servis", "service", "name", "nazvanie"):
        if key in data:
            print("Название сервиса:", data[key])
            break


def task_h2():
    print("\n=== Задача H2. Список анкет ===")
    r = requests.get(BASE + "/anketi", timeout=3)
    anketi = r.json()
    print("Всего анкет пришло:", len(anketi))
    if anketi:
        print("ФИО первой:", anketi[0]["fio"])


def task_h3():
    print("\n=== Задача H3. Анкеты нет ===")
    r = requests.get(BASE + "/anketi/99", timeout=3)
    print("Код ответа:", r.status_code)
    print("r.ok:", r.ok)
    if r.status_code == 404:
        print("Текст ошибки:", r.json().get("oshibka", r.text))


def task_h4():
    print("\n=== Задача H4. Только преподаватели ===")
    r = requests.get(BASE + "/anketi", params={"tip": "t"}, timeout=3)
    print("Адрес запроса:", r.url)
    for prepod in r.json():
        print(f"{prepod['fio']} — {prepod['kafedra']}")


def task_h5():
    print("\n=== Задача H5. Отправка на проверку ===")
    for mail in ["ivanov@mail.ru", "kuznetsov.mail.ru"]:
        r = requests.post(BASE + "/proverka", json={"mail": mail}, timeout=3)
        otvet = r.json()
        print(f"Почта: {mail} | Код: {r.status_code} | prinyato: {otvet.get('prinyato')}")


if __name__ == "__main__":
    task_h1()
    task_h2()
    task_h3()
    task_h4()
    task_h5()
