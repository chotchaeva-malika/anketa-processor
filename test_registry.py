import pytest
from people import Student
from registry import Registry

TEST_DATA = """s;иванов иван петрович;ivanov@mail.ru;+7 (921) 111-22-33;09с33
s;сидоров;sidorov@mail.ru;+79210000000;09с34
s;петрова анна;petrova@yandex.ru;89217654321;09с33
s;кузнецов павел;kuznetsov.mail.ru;+79211234567;09с34
t;лебедева мария сергеевна;lebedeva@gmail.com;8 (911) 222-33-44;Кафедра О7
x;тест тест;test@mail.ru;89211112233;09с33
"""


@pytest.fixture
def filled_registry(tmp_path):
    file_path = tmp_path / "anketa.txt"
    file_path.write_text(TEST_DATA, encoding="utf-8")
    registry = Registry()
    registry.load(file_path)
    return registry


def test_empty_registry_length():
    registry = Registry()
    assert len(registry) == 0


def test_load_valid_records_count(filled_registry):
    assert len(filled_registry) == 3


def test_load_invalid_records_count(filled_registry):
    assert len(filled_registry.decline_anket) == 3


def test_invalid_records_line_numbers(filled_registry):
    line_numbers = [item[0] for item in filled_registry.decline_anket]
    assert line_numbers == [2, 4, 6]


def test_load_nonexistent_file(tmp_path):
    registry = Registry()
    result = registry.load(tmp_path / "missing_file.txt")
    assert result is False
    assert len(registry) == 0


def test_stats_by_role(filled_registry):
    assert filled_registry.stats_by_role() == {"студент": 2, "преподаватель": 1}


def test_stats_by_group_students_only(filled_registry):
    assert filled_registry.stats_by_group() == {"09с33": 2}


def test_iterate_accepted_records(filled_registry):
    names = [person.fio for person in filled_registry.accept_anket]
    assert len(names) == 3


def test_sort_alphabetically():
    registry = Registry()
    registry.add(Student("Яковлев Иван", "yak@mail.ru", "89211112233", "09с33"))
    registry.add(Student("Ёлкин Пётр", "elk@mail.ru", "89211112234", "09с33"))
    registry.add(Student("Абрамов Олег", "abr@mail.ru", "89211112235", "09с33"))
    surnames = [person.fio.split()[0] for person in sorted(registry.accept_anket)]
    assert surnames == ["Абрамов", "Ёлкин", "Яковлев"]


def test_save_ok_writes_one_line_per_person(filled_registry, tmp_path):
    ok_file = tmp_path / "ok.txt"
    filled_registry.save_ok(ok_file)
    lines = ok_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3


def test_save_errors_writes_rejection_reasons(filled_registry, tmp_path):
    err_file = tmp_path / "errors.txt"
    filled_registry.save_errors(err_file)
    content = err_file.read_text(encoding="utf-8")
    assert "в ФИО меньше двух слов" in content
    assert "почта неверная" in content
    assert "неизвестный тип" in content
