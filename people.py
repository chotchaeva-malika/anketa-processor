class AnketaError(Exception):
    pass

class Person:
    def __init__(self, fio_raw, mail_raw, phone_raw):
        self.fio = self.check_fio(fio_raw)
        self.mail = self.check_mail(mail_raw)
        self.phone = self.check_phone(phone_raw)

    @staticmethod
    def check_fio(full_name):
        words = full_name.split()
        if len(words) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        return " ".join(words).title()

    @staticmethod
    def check_mail(input_mail):
        mail = input_mail.strip().lower()
        if mail.count("@") != 1:
            raise AnketaError(f"почта неверная: {input_mail.strip()}")
        name_part, domain = mail.split("@")
        if not name_part or not domain:
            raise AnketaError(f"почта неверная: {input_mail.strip()}")
        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"почта неверная: {input_mail.strip()}")
        return mail

    @staticmethod
    def check_phone(user_number):
        digits = [ch for ch in user_number if ch.isdigit()]
        if len(digits) != 11 or digits[0] not in ("7", "8"):
            raise AnketaError(f"телефон неверный: {user_number.strip()}")
        digits[0] = "7"
        d = "".join(digits)
        return f"+7 ({d[1:4]}) {d[4:7]}-{d[7:9]}-{d[9:11]}"

    def masked_phone(self):
        return f"{self.phone[:9]}***-**-{self.phone[-2:]}"

    def short_fio(self):
        parts = self.fio.split()
        res = parts[0]
        for word in parts[1:]:
            res += f" {word[0]}."
        return res

    def role(self):
        return "—"

    def extra(self):
        return "—"

    def __str__(self):
        return f"{self.fio} ({self.role()}, {self.extra()})"

    def __lt__(self, other):
        return self.fio < other.fio

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.mail == other.mail

    def __hash__(self):
        return hash(self.mail)

class Student(Person):
    def __init__(self, fio_raw, mail_raw, phone_raw, group_raw):
        super().__init__(fio_raw, mail_raw, phone_raw)
        group = group_raw.replace(" ", "").lower()
        if not group:
            raise AnketaError("пустая группа")
        self.group = group

    def role(self):
        return "студент"

    def extra(self):
        return self.group


class Teacher(Person):
    def __init__(self, fio_raw, mail_raw, phone_raw, dept_raw):
        super().__init__(fio_raw, mail_raw, phone_raw)
        dept = " ".join(dept_raw.split())
        if not dept:
            raise AnketaError("пустая кафедра")
        self.dept = dept

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.dept


def parse_line(line):
    parts = line.split(";")
    if len(parts) != 5:
        raise AnketaError(f"полей {len(parts)} вместо 5")

    kind = parts[0].strip().lower()
    fio_raw, mail_raw, phone_raw, extra_raw = parts[1], parts[2], parts[3], parts[4]

    if kind == "s":
        return Student(fio_raw, mail_raw, phone_raw, extra_raw)
    elif kind == "t":
        return Teacher(fio_raw, mail_raw, phone_raw, extra_raw)
    else:
        raise AnketaError(f"неизвестный тип: {kind}")


if __name__ == "__main__":
    pass
