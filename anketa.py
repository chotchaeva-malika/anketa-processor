input_file = "anketa.txt"
accept_file = "ok.txt"
defect_file = "errors.txt"

def check_fio(full_name):
    words = full_name.split()
    if len(words) < 2:
        return None
    done_fio = " ".join(words).title()
    return done_fio

def check_mail(input_mail):
    mail = input_mail.strip().lower()
    if mail.count("@") != 1:
        return None
    
    name_part, domain = mail.split("@")
    if not name_part or not domain:
        return None

    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return None     
    return mail

def check_phone(user_number):
    digits = [ch for ch in user_number if ch.isdigit()]

    if len(digits) != 11:
        return None
    if digits[0] not in ('7', '8'):
        return None
    
    digits[0] = "7"
    d = "".join(digits)
    return f"+7 ({d[1:4]}) {d[4:7]}-{d[7:9]}-{d[9:11]}"

def check_group(user_group):
    group = user_group.replace(" ", "").lower()
    if group == "": return None
    return group

def print_table(accept_anket):
    print(f"{'№':<4}{'ФИО':<28}{'Почта':<22}{'Телефон':<20}{'Группа':<8}")
    print("-" * 82)

    for id, (fio, email, phone, group) in enumerate(accept_anket, start=1):
        short_fio = fio[:26] + "…" if len(fio) > 27 else fio
        masked_phone = f"{phone[:9]}***-**-{phone[-2:]}"
        print(f"{id:<4}{short_fio:<28}{email:<22}{masked_phone:<20}{group:<8}")
    print("-" * 82)

def print_errors(decline_anket):
    print(f"\nОтклонено строк: {len(decline_anket)}")
    for line_num, reason, raw_text in decline_anket:
        print(f"  строка {line_num}: {reason}")
        print(f"      {raw_text}")

def print_summary(total_lines, accept_anket, decline_anket):
    print(f"\nВсего строк в файле: {total_lines}")
    print(f"Принято: {len(accept_anket)} | Отклонено: {len(decline_anket)}")

    stat = {}
    for _, _, _, group in accept_anket:
        stat[group] = stat.get(group, 0) + 1

    print("\nПо группам:")
    for group, count in sorted(stat.items()):
        print(f"  {group:<8}{count}")


def save_results(accept_anket, decline_anket):
    with open(accept_file, "w", encoding="utf-8") as ok_f:
        for fio, mail, phone, group in accept_anket:
            ok_f.write(f"{fio};{mail};{phone};{group}\n")

    with open(defect_file, "w", encoding="utf-8") as err_f:
        for line_num, reason, raw_text in decline_anket:
            err_f.write(f"строка {line_num}: {reason} | {raw_text}\n")

    print(f"\nСохранено: {accept_file} и {defect_file}")

def parse_line(line):
    parts = line.split(";")
    if len(parts) != 4:
        return None, f"полей {len(parts)} вместо 4"

    fio_raw, mail_raw, phone_raw, group_raw = parts

    fio = check_fio(fio_raw)
    if fio is None:
        return None, "в ФИО меньше двух слов"

    mail = check_mail(mail_raw)
    if mail is None:
        return None, f"почта неверная: {mail_raw.strip()}"

    phone = check_phone(phone_raw)
    if phone is None:
        return None, f"телефон неверный: {phone_raw.strip()}"

    group = check_group(group_raw)
    if group is None:
        return None, "пустая группа"

    return (fio, mail, phone, group), None


def main():
    accept_anket = []
    decline_anket = []
    total_lines = 0
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            for line_num, raw_line in enumerate(file, 1):
                total_lines = line_num
                line = raw_line.strip()
                if not line: continue

                anket, error_reason = parse_line(line)
                if error_reason:
                    decline_anket.append((line_num, error_reason, line))
                else:
                    accept_anket.append(anket)
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден!")
        return

    accept_anket.sort(key=lambda a: a[0])
    print_table(accept_anket)
    print_errors(decline_anket)
    print_summary(total_lines, accept_anket, decline_anket)
    save_results(accept_anket, decline_anket)

main()
