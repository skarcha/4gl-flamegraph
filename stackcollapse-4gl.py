#!/usr/bin/env python

from __future__ import print_function
import sys
import re

OUTPUT_TIME = 'time'
OUTPUT_CALLS = 'calls'


def warning(*objs):
        print("WARNING:", *objs, file=sys.stderr)


def print_stack(
        functions, output_type, stack,
        parent_id, call_cost, recursive_call_count):
    if output_type != OUTPUT_CALLS:
        print(';'.join(stack),
              int(call_cost * functions[parent_id][output_type]))

    for child_id, child_data in functions[parent_id]['childs'].items():
        if not functions[child_id]['childs'] or functions[child_id]['dup']:
            print(';'.join(stack+[functions[child_id]['name']]),
                  int(call_cost * child_data[output_type]))
            continue

        # Recursive calls control.
        if child_id == parent_id:
            recursive_call_count += 1
            if (recursive_call_count >
                    functions[parent_id]['childs'][child_id]['calls']):
                recursive_call_count = 0
                return

        print_stack(functions, output_type,
                    stack+[functions[child_id]['name']], child_id,
                    call_cost*child_data['call_cost'], recursive_call_count)


def build_functions_dict(fin):
    functions = {}

    rexp = re.compile('^(\[(\d+)\])*\t\s+([^\s]+)\s+([^\s]+)\s+(\d{1,3}.\d{2})'
                      '\s*(\d+)(\/(\d+))?\s+(.{3})\s(.*)')

    for line in fin:
        fields = rexp.match(line)

        if fields:
            line_type = fields.group(9)
            time = float(fields.group(4).replace(',', '.')) * 1000000
            calls = fields.group(6)
            calls_total = fields.group(8)
            function_name = fields.group(10)

            if calls_total is None:
                calls_total = calls

            function_id = function_name + '_' + calls_total
            calls = int(calls)
            call_cost = float(calls) / float(calls_total)

            if line_type == "***":
                parent_id = function_id
                dup = parent_id in functions

                if dup:
                    warning("%s duplicated object. Skipped!" % parent_id)

                functions[parent_id] = {
                    'name': function_name,
                    'dup': dup,
                    'call_cost': call_cost,
                    OUTPUT_TIME: time,
                    OUTPUT_CALLS: calls,
                    'childs': {}
                }

            elif line_type == "-->":
                # Recursive call
                if parent_id == function_id:
                    continue

                functions[parent_id]["childs"][function_id] = {
                    'name': function_name,
                    'call_cost': call_cost,
                    OUTPUT_TIME: time,
                    OUTPUT_CALLS: calls
                }

    return functions


def collapse():
    params = sys.argv

    if '-ot' in params:
        output_type = OUTPUT_TIME
        params.remove('-ot')

    elif '-oc' in params:
        output_type = OUTPUT_CALLS
        params.remove('-oc')

    else:
        output_type = OUTPUT_TIME

    if len(params) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin

    functions = build_functions_dict(f)

    print_stack(functions, output_type, ["main"], "main_1", 1, 0)


if __name__ == "__main__":
    collapse()
