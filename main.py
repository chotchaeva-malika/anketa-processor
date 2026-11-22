from registry import Registry

def main():
    input_file = "anketa.txt"
    accept_file = "ok.txt"
    defect_file = "errors.txt"

    reg = Registry()
    if not reg.load(input_file):
        print(f"Ошибка: файл {input_file} не найден!")
        return

    print(f"{'№':<4}{'ФИО':<28}{'Роль':<15}{'Группа/кафедра':<16}{'Телефон':<18}")
    print("-" * 81)

    for idx, p in enumerate(sorted(reg.accept_anket), start=1):
        short_fio = p.fio[:26] + "…" if len(p.fio) > 27 else p.fio
        print(f"{idx:<4}{short_fio:<28}{p.role():<15}{p.extra():<16}{p.masked_phone():<18}")

    print("-" * 81)

    print(f"\nОтклонено строк: {len(reg.decline_anket)}")
    for line_num, reason, raw_text in reg.decline_anket:
        print(f"  строка {line_num}: {reason}")
        print(f"      {raw_text}")

    print(f"\nВсего строк в файле: {reg.total_lines}")
    print(f"Принято: {len(reg)} | Отклонено: {len(reg.decline_anket)}")

    print("\nПо ролям:")
    for role, count in sorted(reg.stats_by_role().items()):
        print(f"  {role:<15}{count}")

    print("\nПо группам:")
    for group, count in sorted(reg.stats_by_group().items()):
        print(f"  {group:<15}{count}")

    reg.save_ok(accept_file)
    reg.save_errors(defect_file)
    print(f"\nСохранено: {accept_file} и {defect_file}")

if __name__ == "__main__":
    main()
