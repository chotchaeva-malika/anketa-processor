from validators import parse_line
from report import print_table, print_errors, print_summary

input_file = "anketa.txt"
accept_file = "ok.txt"
defect_file = "errors.txt"

def save_results(accept_anket, decline_anket):
    with open(accept_file, "w", encoding="utf-8") as ok_f:
        for fio, mail, phone, group in accept_anket:
            ok_f.write(f"{fio};{mail};{phone};{group}\n")

    with open(defect_file, "w", encoding="utf-8") as err_f:
        for line_num, reason, raw_text in decline_anket:
            err_f.write(f"строка {line_num}: {reason} | {raw_text}\n")

    print(f"\nСохранено: {accept_file} и {defect_file}")


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

if __name__ == "__main__":
    main()
