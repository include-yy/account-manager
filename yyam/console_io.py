# MIT License

# Copyright (c) 2020 include-yy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import re
import configparser
import os


def input_gen(instr=None, re_str='.*', item_name='', f_check=True):
    if f_check is False:
        if instr is None:
            return ''
        else:
            return re.sub(r'(^\s*)|(\s*$)', '', instr)

    out_str = ''
    if instr is not None:
        out_str = re.sub(r'(^\s*)|(\s*$)', '', instr)
        if re.fullmatch(re_str, out_str) is not None:
            return out_str
        else:
            print(item_name, ':', instr, 'format not correct')
    else:
        f_exit = False
        while not f_exit:
            print('please input', item_name, ':')
            instr = input()
            out_str = re.sub(r'(^\s*)|(\s*$)', '', instr)
            if re.fullmatch(re_str, out_str) is not None:
                return out_str
            elif out_str in [':q', ':q!', ':!q']:
                f_exit = True
            else:
                print(item_name, ': ', 'format not correct, try again')
                continue
    return out_str


def input_website(in_str, f_check=True):
    return input_gen(in_str, '.+', 'website', f_check)


def input_id(in_str, f_check=True):
    return input_gen(in_str, '.+', 'id', f_check)


def input_username(in_str, f_check=True):
    return input_gen(in_str, '.+', 'username', f_check)


def input_password(in_str, f_check=True):
    return input_gen(in_str, '.+', 'password', f_check)


def input_email(in_str, f_check=True):
    return input_gen(in_str, r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', 'email', f_check)


def input_phone_number(in_str, f_check=True):
    return input_gen(in_str, r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'phone number', f_check)


input_func_map = {
    'website': input_website,
    'id': input_id,
    'username': input_username,
    'password': input_password,
    'email': input_email,
    'phone_number': input_phone_number
}


def option_make_set(opt_arr, regex_str):
    receive_array = []
    for x in opt_arr:
        receive_array += re.findall(regex_str, x)
    return set(receive_array)


def input_select(search_arr):
    if len(search_arr) == 1:
        return search_arr[0]

    count = 1
    for x in search_arr:
        print(count, ":")
        print('website :', x[0])
        print('id      :', x[1]['id'])
        print('username:', x[1]['username'])
        count = count + 1

    in_number = input_gen(None, r'\d+', 'order number')
    if in_number in [':q', ':q!', ':!q']:
        print('input_select: quit select\n')
        return False
    in_number = int(in_number)
    if count >= in_number >= 1:
        return search_arr[in_number - 1]
    elif in_number > count:
        return search_arr[-1]
    else:
        return search_arr[0]


def write_config(in_str):
    config = configparser.ConfigParser()
    real_path = '%s/' % os.path.dirname(os.path.realpath(__file__))
    config['DEFAULT'] = {'path': in_str}

    try:
        f = open(real_path + 'config.ini', 'w', encoding='utf-8')
        config.write(f)
    except FileNotFoundError:
        print('config file config.ini not found')
        exit()
    else:
        f.close()

    return True


def read_config():
    config = configparser.ConfigParser()
    real_path = '%s/' % os.path.dirname(os.path.realpath(__file__))
    try:
        f = open(real_path + 'config.ini', encoding='utf-8')
        config.read_file(f)
    except FileNotFoundError:
        print('config file config.ini not found, use -c [filename] option to create one')
        exit()
    else:
        f.close()
    return config['DEFAULT']['path']
