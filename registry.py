from people import AnketaError, parse_line


class Registry:
    def __init__(self):
        self.accept_anket = []
        self.decline_anket = []
        self.total_lines = 0

    def add(self, person):
        self.accept_anket.append(person)

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line_num, raw_line in enumerate(file, start=1):
                    self.total_lines = line_num
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        person = parse_line(line)
                        if person in self.accept_anket:
                            raise AnketaError(f"дубликат почты: {person.mail}")

                        self.add(person)
                    except AnketaError as reason:
                        self.decline_anket.append((line_num, str(reason), line))
            return True
        except FileNotFoundError:
            return False

    def stats_by_role(self):
        stat = {}
        for person in self.accept_anket:
            r = person.role()
            stat[r] = stat.get(r, 0) + 1
        return stat

    def stats_by_group(self):
        stat = {}
        for person in self.accept_anket:
            if person.role() == "студент":
                g = person.extra()
                stat[g] = stat.get(g, 0) + 1
        return stat

    def save_ok(self, accept_file="ok.txt"):
        with open(accept_file, "w", encoding="utf-8") as ok_f:
            for p in sorted(self.accept_anket):
                ok_f.write(f"{p.fio};{p.role()};{p.extra()};{p.mail};{p.phone}\n")

    def save_errors(self, defect_file="errors.txt"):
        with open(defect_file, "w", encoding="utf-8") as err_f:
            for line_num, reason, raw_text in self.decline_anket:
                err_f.write(f"строка {line_num}: {reason} | {raw_text}\n")

    def __len__(self):
        return len(self.accept_anket)


if __name__ == "__main__":
    pass
