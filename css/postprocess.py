#!/usr/bin/env python

import argparse
import re
import os

import_rx = re.compile("^@import url\\('(?P<file>[^']+)'\\);$")
opening_brace_rx = re.compile("^\\s*:root\s*{\\s*$")
closing_brace_rx = re.compile("^\\s*}\\s*$")
comment_rx = re.compile("^\\s*(/\\*.*\\*/)?\\s*$")
variable_declaration_rx = re.compile("^\\s*(?P<key>--[a-z-]+)\\s*:\\s*(?P<value>[^;]+)\\s*;\\s*$")
variable_use_rx = re.compile("^(?P<before>.+)var\\((?P<key>--[a-z-]+)\\)(?P<after>.+)$")

def postprocess(files):
    directory = os.path.dirname(files[0])
    basename, ext = os.path.splitext(files[0])
    out_file = basename + ".compiled" + ext

    with open(out_file, mode='w') as out:
        variables = {}
        imported_files = []

        not_just_variable_declarations = False

        # Put a helper comment on top
        out.write("/* Generated using `./postprocess.py {}`. Do not edit. */\n".format(' '.join(files)))

        # Parse the top-level file
        with open(files[0]) as f:
            in_variable_declarations = False
            for line in f:
                # Import statement: add the file at the beginning of th
                match = import_rx.match(line)
                if match:
                    imported_files += [match['file']]
                    continue

                # Opening brace of variable declaration block
                match = opening_brace_rx.match(line)
                if match:
                    in_variable_declarations = True
                    continue

                # Variable declaration
                match = variable_declaration_rx.match(line)
                if match and in_variable_declarations:
                    variables[match['key']] = match['value']
                    continue

                # Comment or empty line, ignore
                if comment_rx.match(line):
                    continue

                # Closing brace of variable declaration block. If it was not
                # just variable declarations, put the closing brace to the
                # output as well.
                match = closing_brace_rx.match(line)
                if match and in_variable_declarations:
                    if not_just_variable_declarations: out.write("}\n")
                    in_variable_declarations = False
                    continue

                # Something else, copy verbatim to the output. If inside
                # variable declaration block, include also the opening brace
                # and remeber to put the closing brace there as well
                if in_variable_declarations:
                    out.write(":root {\n")
                    not_just_variable_declarations = True
                out.write(line)

        # Now open the imported files and replace variables
        for file in imported_files + files[1:]:
            out.write('\n')

            with open(file) as f:
                for line in f:
                    # Variable use, replace with actual value
                    # TODO: more variables on the same line?
                    match = variable_use_rx.match(line)
                    if match and match['key'] in variables:
                        out.write(match['before'])
                        out.write(variables[match['key']])
                        out.write(match['after'])
                        out.write("\n")
                        continue

                    # Comment or empty line, ignore
                    if comment_rx.match(line):
                        continue

                    # Something else, copy verbatim to the output
                    out.write(line)

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=r"""
Postprocessor for removing @import statements and variables from CSS files.

Combines all files into a new *.compiled.css file. The basename is taken
implicitly from the first argument.""")
    parser.add_argument('files', nargs='+', help='input CSS file(s)')
    args = parser.parse_args()

    exit(postprocess(args.files))
