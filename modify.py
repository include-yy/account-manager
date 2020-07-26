from tomdb import *
from console_io import *


def operation_modify(args, org_dic):
    opt_set = option_make_set(args.modify, r'[upen]')
    if len(opt_set) == 0:
        print('operation_modify: -m arguments not valid')
        return False

    items_map = {}
    for x in input_func_map.keys():
        items_map[x] = input_gen(getattr(args, x), f_check=False)
    search_arr = tomdb_search(items_map, org_dic)
    if not search_arr:
        print('operation_modify: specify item not found')
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
            if items_map[sl_map[x]] == ':q':
                items_map[sl_map[x]] = ''
            elif items_map[sl_map[x]] in [':q!', ':!q']:
                print('operation_modify: quit!')
                return False
            else:
                continue

    return tomdb_update(items_map, target_item[1])
