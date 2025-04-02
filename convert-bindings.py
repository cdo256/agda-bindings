#!/usr/bin/env python3
from pylatexenc.latexencode import unicode_to_latex
import csv

with open("bindings.csv") as file:
    reader = csv.reader(file, delimiter=" ", quotechar='"')
    for row in reader:
        print(", ".join(row))
