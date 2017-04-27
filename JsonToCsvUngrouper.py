import csv
import json

class JsonToCsvUngrouper:

    def __init__(self, csv_file, cols_to_explode):
        self.csv_file = csv_file

        if not hasattr(cols_to_explode, '__iter__'):
            self.cols_to_explode = [cols_to_explode]
        else:
            self.cols_to_explode = cols_to_explode
        self.col_nums_to_explode = []

    def read_csv(self):
        with open(self.csv_file, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='"')
            first_row = lines.next()

            # assume that the first row is column headers
            for i in range(len(first_row)):
                if first_row[i] in self.cols_to_explode:
                    self.col_nums_to_explode.append(i)

