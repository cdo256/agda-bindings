#!/usr/bin/env python3
from os import close
from pylatexenc.latexencode import unicode_to_latex
import csv
import subprocess as sp
import re
import argparse
import sys
import logging

logging.basicConfig(handlers=[logging.FileHandler("output.log")])


def escape(str):
    return str.replace("\\", "\\\\")


def transform_latex(str):
    return re.sub(r"^\\ensuremath\{(.*)\}", r"\1", str)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Argument parser for JSON file generation."
    )

    # Positional argument for output file (optional)
    parser.add_argument(
        "output_file",
        nargs="?",  # Makes it optional
        default=None,
        help="Path to the output JSON file. If not provided, a default file will be generated.",
    )

    # --insert / -i flag
    parser.add_argument(
        "-i",
        "--insert",
        action="store_true",
        help="Flag to enable insertion. Requires an output file.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Validation: If --insert is used, output_file must be provided
    if args.insert and not args.output_file:
        parser.error("The --insert (-i) flag requires an output file to be specified.")

    # Default behavior: if no arguments are provided, set a default output file
    if not args.output_file:
        args.output_file = "default_output.json"

    return args


def extract():
    print("Extracting...")
    sp.run(["just-agda", "--batch", "--script", "extract-bindings.el"])


def convert():
    with open("bindings.csv") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        rows = list(reader)
    print(f"Converting {len(rows)} entries...")
    sequence_map = {}
    for row in rows:
        # Track last index
        try:
            sequence_map[row[0]] = int(row[3])
        except:
            pass
    output = []
    for row in rows:
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
                else f"{index:01}" if duplicity < 10 else f"{index:02}"
            )
            auto_flag = "A" if len(sequence) > 2 else ""
            if '"' in sequence:
                # FIXME: Quotes may require escape the csv in the elisp code.
                continue

            # Produce bindings for both math and text mode.
            output.append(
                f'    {{trigger: "{escape(sequence)}{suffix}", replacement: "{escape(latex)}", options: "m{auto_flag}"}},'
            )
            output.append(
                f'    {{trigger: "{escape(sequence)}{suffix}", replacement: "${escape(latex)}$", options: "t{auto_flag}"}},'
            )
        except Exception as e:
            pass

    return output


def find_str_in_lines(pattern, lines):
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            return i


def read_lines(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()


def write_lines(filename, lines, mode):
    with open(filename, mode) as file:
        file.seek(0)
        file.truncate()
        file.writelines(map(lambda line: line + "\n", lines))


def insert(filename, lines_to_insert):
    print(f"Inserting {len(lines_to_insert)} lines into {filename}.")
    lines_to_insert = (
        ["    //BEGIN_AGDA_BINDINGS"] + lines_to_insert + ["    //END_AGDA_BINDINGS"]
    )
    file_lines = read_lines(filename)
    start_index = find_str_in_lines("BEGIN_AGDA_BINDINGS", file_lines)
    end_index = find_str_in_lines("END_AGDA_BINDINGS", file_lines)
    close_bracket = find_str_in_lines(r"^\]", file_lines)
    if start_index and end_index:
        lines = file_lines[:start_index] + lines_to_insert + file_lines[end_index:]
    elif close_bracket:
        lines = file_lines[:end_index] + lines_to_insert + file_lines[end_index:]
    else:
        raise Exception(
            "Close bracket ']' not found in file. It must be on its own line for it to be recognized."
        )
    write_lines(filename, lines, "w")


def replace_file(filename, lines):
    print(f"Replacing {filename} with {len(lines)} lines")
    lines = ["["] + lines + ["]"]
    write_lines(filename, lines, "x")


def main():
    args = parse_arguments()
    extract()
    lines = convert()
    lines.insert(
        0, "    // Automatically generated via https://github.com/cdo256/agda-bindings."
    )
    if args.insert:
        insert(args.output_file, lines)
    else:
        replace_file(args.output_file, lines)


if __name__ == "__main__":
    main()
