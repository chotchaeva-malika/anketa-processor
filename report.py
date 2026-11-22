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


if __name__ == "__main__":
    pass
