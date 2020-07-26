import argparse
import toml
from add import operation_add
from modify import operation_modify
from delete import operation_delete
from search import operation_search
from list_item import operation_list, operation_list_all
from tomdb import tomdb_read, tomdb_write
# import sys


def parser_init():
    parser = argparse.ArgumentParser(description='account info manager',
                                     epilog='author: include-yy, last modified time: 2020.7.26 utc+8')
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
    type_array = ['add', 'modify', 'delete', 'search', 'list', 'list_all']
    for x in type_array:
        if getattr(args, x) is not False:
            return x
    return False


def main():
    default_dir_path = 'new.txt'

    parser = parser_init()
    input_args = parser.parse_args()

    f = None
    try:
        if input_args.filename is not None:
            f = open(input_args.filename, encoding='utf-8')
        else:
            f = open(default_dir_path, encoding='utf-8')
    except FileNotFoundError:
        print('file not found: no such file or directory\n')
        exit()

    org_dic = {}
    try:
        org_dic = tomdb_read(f)
    except TypeError:
        print('type error\n')
        exit()
    except toml.TomlDecodeError:
        print('file format error\n')
        exit()
    else:
        f.close()

    type_check = operation_type_check(input_args)
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
        # tomdb_write(org_dic, sys.stdout)
        print('success')
    else:
        print('fail')
        exit()

    try:
        f = open('new.txt', 'w', encoding='utf-8')
    except FileNotFoundError:
        print('file not found: no such file or directory: 2\n')
        exit()

    try:
        tomdb_write(org_dic, f)
    except TypeError:
        print('type error\n')
        exit()
    except toml.TomlDecodeError:
        print('file format error\n')
        exit()
    else:
        f.close()


if __name__ == '__main__':
    main()
