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


import argparse
import toml
from .add import operation_add
from .modify import operation_modify
from .delete import operation_delete
from .search import operation_search
from .list_item import operation_list, operation_list_all
from .tomdb import tomdb_read, tomdb_write
from .console_io import read_config, write_config


def parser_init():
    parser = argparse.ArgumentParser(description='yyam: account info manager',
                                     epilog='author: include-yy, last modified time: 2020.7.28, 11:00, utc+8')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-a', '--add', metavar='items', nargs='+', default=False,
                       help='add new item, it can be website(w), username(u), '
                            'password(p), email(e) and phone-number(n) [wupen]+')
    group.add_argument('-m', '--modify', metavar='items', nargs='+', default=False,
                       help='modify exist items, it can be username(u), '
                            'password(p), email(e) and phone-number(n) [upen]+')
    group.add_argument('-d', '--delete', metavar='items', nargs='+', default=False,
                       help='delete exist items, it can be website(w), id(i), '
                            'username(u), password(p), email(e) and phone number(n) [wuipen]+')
    group.add_argument('-s', '--search', metavar='items', nargs='*', default=False,
                       help='search exist items, it can be website(w), id(i), '
                            'username(u), password(p) email(e) and phone-number(n). or just no args [wuipen]*')
    group.add_argument('-l', '--list', action='store_true',
                       help='list website info, include website, id, username')
    group.add_argument('-la', '--list-all', action='store_true',
                       help='list all website info, include password, email and phone number')
    group.add_argument('-c', '--configure', metavar='file-path', default=False,
                       help='configure the default file path')

    parser.add_argument('-w', '--website', metavar='website', help='specify website')
    parser.add_argument('-i', '--id', metavar='id', help='specify id')
    parser.add_argument('-u', '--username', metavar='name', help='specify username')
    parser.add_argument('-p', '--password', metavar='password', help='specify password')
    parser.add_argument('-e', '--email', metavar='email', help='specify email')
    parser.add_argument('-n', '--phone-number', metavar='phone', help='specify phone number')

    parser.add_argument('-f', '--filename', metavar='filename', help='specify file to read (optional)')
    parser.add_argument('-o', '--output-file', metavar='filename', help='specify output file (optional)')
    return parser


def operation_type_check(args):
    type_array = ['add', 'modify', 'delete', 'search', 'list', 'list_all', 'configure']
    for x in type_array:
        if getattr(args, x) is not False:
            return x
    return False


def main():
    parser = parser_init()
    input_args = parser.parse_args()
    type_check = operation_type_check(input_args)

    if not type_check:
        print('yyam: no option specified. quit',
              'type -h or --help for help')
        exit()
    elif type_check != 'configure':
        pass
    else:
        write_config(input_args.configure)
        exit()

    default_dir_path = read_config()
    org_dic = {}
    try:
        if input_args.filename is not None:
            org_dic = tomdb_read(input_args.filename)
        else:
            org_dic = tomdb_read(default_dir_path)
    except FileNotFoundError:
        print('file not found: no such file or directory')
        exit()
    except TypeError:
        print('toml: type error')
        exit()
    except toml.TomlDecodeError:
        print('toml: file format error')
        exit()

    if type_check == 'add':
        f_success = operation_add(input_args, org_dic)
    elif type_check == 'modify':
        f_success = operation_modify(input_args, org_dic)
    elif type_check == 'delete':
        f_success = operation_delete(input_args, org_dic)
    elif type_check == 'search':
        f_success = operation_search(input_args, org_dic)
    elif type_check == 'list':
        f_success = operation_list(input_args, org_dic)
    elif type_check == 'list_all':
        f_success = operation_list_all(input_args, org_dic)
    else:
        f_success = False

    if f_success:
        if type_check in ['search', 'list', 'list_all']:
            pass
        else:
            if input_args.output_file is not None:
                tomdb_write(input_args.output_file, org_dic)
            else:
                tomdb_write(default_dir_path, org_dic)
        print('operation', type_check, 'successfully finished')
    else:
        print('operation', type_check, 'failed')


if __name__ == '__main__':
    main()
