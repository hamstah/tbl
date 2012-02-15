import re

class Tbl:

    def __init__(self):
        self.rows = []
        self.max_columns = 0
        self.has_data=False
        self.format = ""
        self.separator = ""
        self.width = []
        self.precision = 4
        self.sort = None
        self.separators = []

    # true if the row is actual data
    def is_data(self, row):
        return not (isinstance(row,str) and (row == "--" or row.startswith("@")))

    def add_row(self, row):

        # cleans and stores data rows
        if self.is_data(row):
            if not self.has_data:
                row = row.title()

            row = [c.strip() for c in row.split(",")]
            self.max_columns = max(self.max_columns, len(row))

            missing  = self.max_columns - len(self.width)
            if missing > 0:
                self.width += [0]*missing

            reg_int = re.compile("^[0-9]+$")
            reg_float = re.compile("^[0-9]+\.[0-9]*$")

            for i in range(0,len(row)):
                self.width[i] = max(self.width[i], len("%s"%(row[i])))
                if re.match(reg_int, row[i]):
                    row[i] = int(row[i])
                elif re.match(reg_float, row[i]):
                    row[i] = round(float(row[i]),self.precision)

            self.rows.append(row)
            self.has_data = True

        # separators
        elif row == "--":
            self.separators.append(len(self.rows))

        #p parameters
        elif not self.has_data:
            try:
                if row.startswith("@width"):
                    r = row.split(",")
                    r[0] = r[0][6:]
                    self.width = [int(x) for x in r]
                elif row.startswith("@precision"):
                    r = row.split(" ")
                    if len(r) == 2:
                        self.precision = int(r[1])
                elif row.startswith("@sort ") or row.startswith("@rsort "):
                    r = row.split(",")
                    r[0] = r[0][6:]
                    self.sort = {"order":[int(x) for x in r],
                                 "reverse":row.startswith("@rsort")}
            except Exception as e:
                pass
        
    def rows_count(self):
        return len(self.rows)
        
    def columns_count(self):
        return self.max_columns

    def sortfn(self):
        return lambda x : tuple([x[o] for o in self.sort["order"]])

    def sort_rows(self, rows):
        if self.sort == None:
            return rows
        if len(self.sort["order"]) == 0 or len(self.sort["order"]) > self.max_columns:
            return rows
        for s in self.sort["order"]:
            if s >= self.max_columns or s < 0:
                return rows

        return sorted(rows, key=self.sortfn(), reverse=self.sort["reverse"]) 

    def output(self):
        if len(self.rows) == 0:
            return
        
        if self.format == "" or self.separator == "":
            (self.separator, self.format) = self.generate_sep_format(self.width)
            
        rows = [self.rows[0]]+self.sort_rows(self.rows[1:])

        print self.separator
        for i in range(len(self.rows)):
            if i in self.separators:
                print self.separator

            p = ["",]*self.max_columns
            p[0:len(rows[i])] = rows[i]
            print self.format%(tuple(p))

        print self.separator

    # generate separator and format str
    def generate_sep_format(self,width):
        format = "|"
        sep = "+"
        for c in range(0,self.max_columns):
            format += " %%%ds |"%(width[c])
            sep += "-"*(width[c]+2)+"+"
        return (sep,format)

class TblLoader:

    @staticmethod
    def load(filename):
        tables = [Tbl()]
        f = open(filename)
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                if tables[-1].rows_count() != 0:
                    tables.append(Tbl())
                continue
            tables[-1].add_row(line)
            
        if tables[-1].rows_count() == 0:
            return tables[0:-1]
        return tables

tables = TblLoader.load("data.tbl")
for table in tables:
    table.output()
    print
