"""
"""

import sys
import re
import shutil

import json

if len(sys.argv) < 3:
    print('Not enough input arguments')
    exit()

################################################################################
# Options

comment = {'begin':'<!--', 'end':'-->'}

################################################################################

errors = []

in_file_path = sys.argv[1]
out_file_path = in_file_path
data_file_path = sys.argv[2]
if len(sys.argv) >= 4:
    out_file_path = sys.argv[3]
else:
    shutil.copyfile(out_file_path, out_file_path + '.tpl')

# Data
json1_file = open(data_file_path)
json1_str = json1_file.read()
data = json.loads(json1_str)

in_file = open(in_file_path)
in_lines = in_file.readlines()

out_lines = []

for in_line in in_lines:

    if '<REPLACED>' in in_line or '<IGNORE>' in in_line or '<ERROR>' in in_line:
        continue

    # Find patterns
    out_lines.append(in_line)
    prog = re.compile(r'<REPLACE:([a-zA-Z0-9_]+)>')
    key_list = prog.findall(in_line)

    # Find
    number_of_elem = 0
    is_list = False
    is_valid_list = False
    for key in key_list:
        if key in data and isinstance(data[key], list):
            if is_list:
                is_valid_list = is_valid_list and (len(data[key])==number_of_elem)
            else:
                number_of_elem = len(data[key])
                is_valid_list = True
            is_list = True
    number_of_loop = number_of_elem
    if number_of_loop == 0:
        number_of_loop = 1
    if is_list and not is_valid_list:
        number_of_loop = 0
        error = '<ERROR> Data list length are not consistent.'
        errors.append(error)
        out_lines.append(comment['begin'] + ' ' + error + comment['end'] + '\n')
    for i in range(0,number_of_loop):
        out_line = in_line
        out_line = re.sub(r'^ *' + comment['begin'] + ' *(.*)' + comment['end'] + ' *', '\g<1>', out_line)
        out_line = out_line.replace('\n', '')
        for key in key_list:
            if key in data:
                if isinstance(data[key], list):
                    value = data[key][i]
                else:
                    value = data[key]
                out_line = out_line.replace('<REPLACE:' + key + '>', str(value))
            else:
                out_line = out_line.replace('<REPLACE:' + key + '>', '')
        if len(key_list) > 0:
            if key in data:
                out_lines.append(out_line + ' '  + comment['begin'] + ' <REPLACED> ' + comment['end'] + '\n')
            else:
                error = '<ERROR> Key \'' + key + '\' not exiting.';
                errors.append(error)
                out_lines.append(comment['begin'] + ' ' + error + ' ' + comment['end'] + '\n')

out_file = open(out_file_path, 'w')
for out_line in out_lines:
    out_file.write(out_line)

if len(errors) > 0:
    print('\n***ERRORS***\n')
    print(str(len(errors)) + ' errors in templating process:')
    for error in errors:
        print('\t' + error)
else:
    print('No error in templating process')
