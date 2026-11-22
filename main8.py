import json
from people import Student, Teacher, AnketaError
from registry import Registry
import client


def dict_to_person(item):
    role_code = str(item.get("tip", "")).strip().lower()
    fio = str(item.get("fio", ""))
    mail = str(item.get("mail", ""))
    phone = str(item.get("phone", ""))

    if role_code == "s":
        group = str(item.get("gruppa", ""))
        return Student(fio, mail, phone, group)
    elif role_code == "t":
        dept = str(item.get("kafedra", ""))
        return Teacher(fio, mail, phone, dept)
    else:
        raise AnketaError(f"неизвестный тип: {role_code}")


def main():
    reg = Registry()
    source_name = ""
    server_stats = None
    server_available = False

    try:
        raw_records = client.get_anketi()
        server_stats = client.get_statistics()
        server_available = True
        source_name = "сервер (http://127.0.0.1:5000)"
        print(f"Данные успешно получены с источника: {source_name}")
        print(f"С сервера получено записей: {len(raw_records)}\n")

        for item in raw_records:
            record_num = item.get("nomer", "?")
            try:
                person = dict_to_person(item)
                reg.add(person)
            except AnketaError as reason:
                reg.decline_anket.append((record_num, str(reason), str(item)))

    except client.ServerNedostupen as err:
        print(f"Сервер недоступен: {err}")
        backup_file = "anketa.txt"
        print(f"Переключаюсь на запасной источник: {backup_file}")
        if not reg.load(backup_file):
            print(f"Ошибка: запасной файл {backup_file} также не найден! Завершение работы.")
            return
        source_name = f"запасной файл ({backup_file})"
        print(f"Данные успешно загружены из источника: {source_name}\n")

    print("ПРИНЯТЫЕ АНКЕТЫ")
    print(f"{'№':<4}{'ФИО':<28}{'Роль':<15}{'Группа/кафедра':<16}{'Телефон':<18}")
    print("-" * 81)
    for idx, person in enumerate(sorted(reg.accept_anket), start=1):
        short_fio = person.fio[:26] + "…" if len(person.fio) > 27 else person.fio
        print(f"{idx:<4}{short_fio:<28}{person.role():<15}{person.extra():<16}{person.masked_phone():<18}")
    print("-" * 81)

    print(f"\nПринято: {len(reg)} | Отклонено: {len(reg.decline_anket)}")

    print("\nОтклонено:")
    for record_num, reason, _ in reg.decline_anket:
        print(f"  №{record_num}: {reason}")

    print("\nСводка по ролям (после проверки клиента):")
    role_stats = reg.stats_by_role()
    for role, count in sorted(role_stats.items()):
        print(f"  {role:<15}{count}")

    if server_stats is not None:
        print("\nСтатистика с сервера (без валидации):")
        for key, val in server_stats.items():
            print(f"  {key}: {val}")

    mail_checks = []
    if server_available:
        print("\nПроверка почты принятых анкет на сервере:")
        for person in sorted(reg.accept_anket):
            try:
                is_accepted = client.check_mail(person.mail)
                status_str = "принята" if is_accepted else "отклонена"
                print(f"  {person.mail:<25} -> {status_str}")
                mail_checks.append({"mail": person.mail, "accepted": is_accepted})
            except client.ServerNedostupen as err:
                print(f"  {person.mail:<25} -> ошибка проверки ({err})")
                break

    report_data = {
        "source": source_name,
        "accepted_total": len(reg),
        "declined_total": len(reg.decline_anket),
        "stats_by_role": role_stats,
        "server_stats": server_stats,
        "accepted_records": [
            {
                "fio": person.fio,
                "role": person.role(),
                "extra": person.extra(),
                "mail": person.mail,
                "phone": person.phone,
            }
            for person in sorted(reg.accept_anket)
        ],
        "declined_records": [
            {"number": record_num, "reason": reason}
            for record_num, reason, _ in reg.decline_anket
        ],
        "mail_checks": mail_checks,
    }

    with open("otchet.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print("\nИтоговый отчёт сохранён в файл otchet.json")


if __name__ == "__main__":
    main()
