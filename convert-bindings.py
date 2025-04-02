#!/usr/bin/env python3
from pylatexenc.latexencode import unicode_to_latex
import csv
import subprocess as sp
import re


def escape(str):
    return str.replace("\\", "\\\\")


def transform_latex(str):
    return re.sub(r"^\\ensuremath\{(.*)\}", r"\1", str)


def extract():
    sp.run(["just-agda", "--batch", "--script", "extract-bindings.el"])


def convert():
    with open("bindings.csv") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        rows = list(reader)
        sequence_map = {}
        for row in rows:
            # Track last index
            try:
                sequence_map[row[0]] = int(row[3])
            except:
                pass
        for row in rows:
            # print(", ".join(row))
            try:
                sequence = row[0]
                character = row[1]
                unicode = row[2]
                index = int(row[3])
                # See for how to add more conversion rules: https://github.com/phfaist/pylatexenc/blob/73eca0574eb1fa2b02293587d4b8f5533e6c0d5f/pylatexenc/latexencode/_uni2latexmap.py
                latex = unicode_to_latex(character)
                latex = transform_latex(latex)
                duplicity = sequence_map[sequence]
                suffix = (
                    ""
                    if duplicity == 1
                    else f"{index:1d}" if duplicity < 10 else f"{index:2d}"
                )
                auto_flag = "A" if len(sequence) > 2 else ""
                # Produce bindings for both math and text mode.
                print(
                    f'    {{trigger: "{escape(sequence)}{suffix}", replacement: "{escape(latex)}", options: "m{auto_flag}"}},'
                )
                print(
                    f'    {{trigger: "{escape(sequence)}{suffix}", replacement: "${escape(latex)}$", options: "t{auto_flag}"}},'
                )
            except Exception as e:
                pass


if __name__ == "__main__":
    print("Extracting...")
    extract()
    print("Converting...")
    convert()  # print(e)
