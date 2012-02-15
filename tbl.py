#!/usr/bin/env python
import re
import sys
from optparse import OptionParser

class Format:
    Title = 0
    Centered = 1   

    valid_formats = {"title":Title}

class Layout:
    Header = 0
    Empty = 1
    Matrix = 2

    valid_layouts = {"header":Header, "empty":Empty, "matrix":Matrix}

class Row(list):
    pass

class Tbl:

    default_splitter = ","

    def __init__(self,parameters = {}):
        self.rows = []
        self.max_columns = 0
        self.has_data=False
        self.format = ""
        self.separator = ""
        self.width = []
        self.precision = 4
        self.sort = None
        self.separators = set()
        self.layout = Layout.Header
        self.header_format = set([Format.Title])
        self.queued_comments = []
        self.extras = {"before":[]}
        self.parameters = parameters
        self.is_splitter_regex = False

        if self.parameters.regex_splitter:
            self.splitter = re.compile(self.parameters.regex_splitter)
            self.is_splitter_regex = True
        elif self.parameters.splitter:
            self.splitter = self.parameters.splitter
        else:
            self.splitter = self.default_splitter
        
            

    # true if the row is actual data
    def is_data(self, row):
        return not (isinstance(row,str) and (row == "--" or row.startswith("@") or row.startswith("#")))

    def split_data(self, row):
        if self.is_splitter_regex:
            return [c.strip() for c in re.split(self.splitter, row)]
        else:
            return [c.strip() for c in row.split(self.splitter)]

    def add_row(self, row):

        # cleans and stores data rows
        if self.is_data(row):
            row = self.split_data(row)

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

            nr = Row(row)
            nr.comments = self.queued_comments
            self.queued_comments = []

            self.rows.append(nr)
            self.has_data = True

        # separators
        elif row == "--":
            if not self.has_data and len(self.queued_comments):
                self.extras["before"] += self.queued_comments
                self.queued_comments = []
            else:
                self.separators.add(len(self.rows))
        # comments
        elif row.startswith("#"):
            if len(row) == 1:
                self.queued_comments.append("")
            else:
                self.queued_comments.append(row[1:])
            return
            
        # parameters
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
                elif row.startswith("@layout "):
                    r = row[8:]
                    if r in Layout.valid_layouts:
                        self.layout = Layout.valid_layouts[r]

            except Exception as e:
                pass
        
    def rows_count(self):
        return len(self.rows)
        
    def columns_count(self):
        return self.max_columns

    def sortfn(self):
        return lambda x : tuple([(x[o] if len(x)>o else "" )for o in self.sort["order"]])

    def sort_rows(self, rows):
        if self.sort == None:
            return rows
        print self.sort["order"]

        if len(self.sort["order"]) == 0 or len(self.sort["order"]) >= self.max_columns:
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
            
        rows = []

        if self.layout == Layout.Header:
            rows = [self.rows[0]]+self.sort_rows(self.rows[1:])

            if 1 not in self.separators:
                self.separators.add(1)
            if Format.Title in self.header_format:
                for i in range(len(rows[0])):
                    if isinstance(rows[0][i],str):
                        rows[0][i] = rows[0][i].title()
        else:
            rows = self.sort_rows(self.rows)

        if self.layout == Layout.Matrix:
            self.separators = set(range(1,len(rows)))
        
        for line in self.extras["before"]:
            print line

        if 0 not in self.separators:
            print self.separator
        for i in range(len(self.rows)):
            if i in self.separators:
                print self.separator
            print self.format_row(rows[i])+"".join(rows[i].comments)
        print self.separator        


    def format_row(self, row):
        p = ["",]*self.max_columns
        p[0:len(row)] = row
        return self.format%(tuple(p))

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
    def load(f, parameters):
        tables = [Tbl(parameters)]
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                if tables[-1].rows_count() != 0:
                    tables.append(Tbl(parameters))
                continue
            tables[-1].add_row(line)
            
        if tables[-1].rows_count() == 0:
            return tables[0:-1]
        return tables

if __name__ == "__main__":
    tables = []

    parser = OptionParser()
    parser.add_option("-s", "--splitter",dest="splitter",
                      help="Fields splitter")
    parser.add_option("-r","--regex-splitter",dest="regex_splitter", help="Regex to separate fields")
    

    (options, args) = parser.parse_args()

    if options.splitter and options.regex_splitter:
        parser.error("-s and -r are mutually exclusive")
    

    if len(args) == 0:
        tables = TblLoader.load(sys.stdin,options)
    else:
        for f in args:
            tables += TblLoader.load(open(f),options)

    for table in tables:
        table.output()
        print
