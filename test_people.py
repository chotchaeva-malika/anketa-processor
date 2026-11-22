import pytest
from people import AnketaError, Person, Student, Teacher, parse_line


@pytest.mark.parametrize("raw_name, expected", [
    ("иванов иван петрович", "Иванов Иван Петрович"),
    ("  ПЕТРОВА   АННА  ", "Петрова Анна"),
    ("сИдОрОв пЕтР", "Сидоров Петр"),
    ("   лебедева   мария  сергеевна ", "Лебедева Мария Сергеевна"),
    ("петров-водкин кузьма", "Петров-Водкин Кузьма"),
])
def test_clean_fio_valid(raw_name, expected):
    assert Person.check_fio(raw_name) == expected


def test_clean_fio_single_word_raises():
    with pytest.raises(AnketaError):
        Person.check_fio("Сидоров")


@pytest.mark.parametrize("raw_mail, expected", [
    ("IvAnov@Mail.Ru", "ivanov@mail.ru"),
    ("  LEBEDEVA@GMAIL.COM  ", "lebedeva@gmail.com"),
])
def test_check_mail_valid(raw_mail, expected):
    assert Person.check_mail(raw_mail) == expected


@pytest.mark.parametrize("invalid_mail", [
    "kuznetsov.mail.ru",
    "morozova@mail,ru",
    "sokolov@.ru",
    "",
    "iv anov@mail.ru",
])
def test_check_mail_invalid(invalid_mail):
    with pytest.raises(AnketaError):
        Person.check_mail(invalid_mail)


@pytest.mark.parametrize("raw_phone", [
    "+7 (921) 111-22-33",
    "89211112233",
    "8 921 111 22 33",
    "79211112233",
])
def test_check_phone_valid(raw_phone):
    assert Person.check_phone(raw_phone) == "+7 (921) 111-22-33"


@pytest.mark.parametrize("invalid_phone", [
    "+7921123",
    "7921",
    "99211112233",
    "телефон",
])
def test_check_phone_invalid(invalid_phone):
    with pytest.raises(AnketaError):
        Person.check_phone(invalid_phone)


def test_masked_phone():
    person = Person("Иванов Иван", "ivanov@mail.ru", "89211112233")
    assert person.masked_phone() == "+7 (921) ***-**-33"


def test_short_fio():
    person = Person("Иванов Иван Петрович", "ivanov@mail.ru", "89211112233")
    assert person.short_fio() == "Иванов И. П."


def test_roles_differ():
    student = Student("Иванов Иван", "ivanov@mail.ru", "89211112233", "09с33")
    teacher = Teacher("Смирнова Ольга", "smirnova@inbox.ru", "89211112233", "Кафедра И4")
    assert student.role() == "студент"
    assert teacher.role() == "преподаватель"
    assert student.role() != teacher.role()


def test_student_empty_group_raises():
    with pytest.raises(AnketaError):
        Student("Волков Денис", "volkov@mail.ru", "+79219998877", "   ")


def test_parse_line_student():
    person = parse_line("s;петрова анна;petrova@yandex.ru;89217654321;09с33")
    assert isinstance(person, Student)
    assert person.fio == "Петрова Анна"
    assert person.group == "09с33"


def test_parse_line_teacher():
    person = parse_line("t;Смирнова Ольга;smirnova@inbox.ru;+79211234567;Кафедра И4")
    assert isinstance(person, Teacher)
    assert person.fio == "Смирнова Ольга"
    assert person.dept == "Кафедра И4"


@pytest.mark.parametrize("invalid_line", [
    "x;тест тест;test@mail.ru;89211112233;09с33",
    "s;орлов иван;orlov@mail.ru;09с38",
    "",
])
def test_parse_line_invalid(invalid_line):
    with pytest.raises(AnketaError):
        parse_line(invalid_line)
