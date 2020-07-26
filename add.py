from console_io import *
from tomdb import *


def operation_add(args, org_dic):
    opt_set = option_make_set(args.add, '[wupen]')
    if len(opt_set) == 0 or ('w' in opt_set and len(opt_set) != 1):
        print('operation_add: -a arguments not valid')
        return False
    elif 'w' in opt_set:
        return operation_add_new(args, opt_set, org_dic)
    else:
        return operation_add_add(args, opt_set, org_dic)


def operation_add_new(args, opt_set, org_dic):
    items_map = {}
    for x in input_func_map.keys():
        items_map[x] = input_func_map[x](getattr(args, x))
        if items_map[x] == ':q':
            if x not in ['website', 'id']:
                items_map[x] = ''
                continue
            else:
                print('operation_add_new: quit')
                return False
        elif items_map[x] in [':q!', ':!q']:
            print('operation_add_new: quit!')
            return False
        else:
            continue
    return tomdb_new(items_map, org_dic)


def operation_add_add(args, opt_set, org_dic):
    items_map = {}
    for x in input_func_map.keys():
        items_map[x] = input_gen(getattr(args, x), f_check=False)
    search_arr = tomdb_search(items_map, org_dic)
    if not search_arr:
        print('operation_add_add: specify item not found')
        return False

    target_item = input_select(search_arr)
    sl_map = {'u': 'username',
              'p': 'password',
              'e': 'email',
              'n': 'phone_number'}

    for x in items_map.keys():
        items_map[x] = ''

    for x in sl_map.keys():
        if x in opt_set:
            items_map[sl_map[x]] = input_func_map[sl_map[x]](getattr(args, sl_map[x]))

    return tomdb_add(items_map, target_item[1])
