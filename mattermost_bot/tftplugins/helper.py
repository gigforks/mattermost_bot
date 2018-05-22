class Table:
    def __init__(self, fields):
        self.rows = 0
        self.output = "|"
        self.dash_line = "\n|"
        for field in fields:
            self.output += "{} |".format(field)
            self.dash_line += ":{}|".format("-" * len(field))
        self.output += self.dash_line

    def add_row(self, fields):
        self.rows += 1
        row = "\n|"
        for field in fields:
            row += "{} |".format(field)
        self.output += row

    def __str__(self):
        if self.rows:
            return self.output
        else:
            return "No results found"
