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


if __name__ == "__main__":
    pass
