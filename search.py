from tomdb import *
from console_io import *


def operation_search(args, org_dic):
    opt_set = option_make_set(args.search, r'[wuipen]')

    items_map = {}
    for x in input_func_map.keys():
        items_map[x] = input_gen(getattr(args, x), f_check=False)
    search_arr = tomdb_search(items_map, org_dic)
    if not search_arr:
        print('operation_search: not found')
        return False

    for x in search_arr:
        if opt_set == set():
            print('website :', x[0])
            print('id      :', x[1]['id'])
            print('username:', x[1]['username'])
        else:
            if 'w' in opt_set:
                print('website     :', x[0])
            if 'i' in opt_set:
                print('id          :', x[1]['id'])
            if 'u' in opt_set:
                print('username    :', x[1]['username'])
            if 'p' in opt_set:
                print('password    :', x[1]['password'])
            if 'e' in opt_set:
                print('email       :', x[1]['email'])
            if 'n' in opt_set:
                print('phone number:', x[1]['phone_number'])
    return True
