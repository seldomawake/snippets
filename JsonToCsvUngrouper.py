import csv
import json


class JsonToCsvUngrouper:

    def __init__(self, csv_file, cols_to_explode):
        self.csv_file = csv_file
        self.raw_rows = None
        self.col_headers = None

        if not hasattr(cols_to_explode, '__iter__'):
            self.cols_to_explode = [cols_to_explode]
        else:
            self.cols_to_explode = cols_to_explode
        self.col_nums_to_explode = []

    def get_exploded_rows(self):
        with open(self.csv_file, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='"')
            first_row = lines.next()
            for row in lines:
                self.reset_col_headers()
                ungrouped_rows = self.explode_rows(rows=[row], col_nums_to_explode_by=self.col_nums_to_explode)
                toret = iter(ungrouped_rows)

                #yield from toret
                for t in toret:
                    yield t

    def reset_col_headers(self):
        if self.col_headers is None:
            with open(self.csv_file, 'rb') as csvfile:
                lines = csv.reader(csvfile, delimiter=',', quotechar='"')
                # assume that the first row is column headers
                self.col_headers = lines.next()

        for i in range(len(self.col_headers)):
            if self.col_headers[i] in self.cols_to_explode:
                self.col_nums_to_explode.append(i)

    def explode_rows(self, rows, col_nums_to_explode_by):
        assert isinstance(col_nums_to_explode_by, list)
        assert isinstance(rows, list)

        if len(col_nums_to_explode_by) == 0:
            return rows

        unwrapped_rows = []
        col_to_explode = col_nums_to_explode_by.pop()

        for row in rows:
            a_row_without_col_to_explode = [v for k, v in enumerate(row) if k != col_to_explode]

            # cols to ungroup by are assumed to be in json objects -- can improve this further
            # (if the .loads throws, assume it is an array of strings with len 1.)
            exploded_col_as_list = json.loads(row[col_to_explode])

            for elem in exploded_col_as_list:
                row_with_exploded_col = a_row_without_col_to_explode[:]
                row_with_exploded_col.insert(col_to_explode, elem)
                unwrapped_rows.append(row_with_exploded_col)

        unwrap_more = self.explode_rows(unwrapped_rows, col_nums_to_explode_by)

        return unwrap_more
