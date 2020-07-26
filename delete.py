from tomdb import *
from console_io import *


def operation_delete(args, org_dic):
    opt_set = option_make_set(args.delete, r'[wiupen]')
    if len(opt_set) == 0:
        print('operation_delete: -d arguments not valid\n')
        return False
    elif 'w' in opt_set and 'i' in opt_set:
        print('operation_delete: -d conflict options: w i\n')
    items_map = {}
    for x in input_func_map.keys():
        items_map[x] = input_gen(getattr(args, x), f_check=False)
    search_arr = tomdb_search(items_map, org_dic)
    if not search_arr:
        print('operation_delete: specify item not found\n')
        return False

    target_item = input_select(search_arr)

    for x in items_map.keys():
        items_map[x] = ''

    items_map['website'] = target_item[0]
    for x in input_func_map.keys():
        if x == 'website':
            continue
        items_map[x] = target_item[1][x]

    sl_map = {'w': 'website',
              'i': 'id',
              'u': 'username',
              'p': 'password',
              'e': 'email',
              'n': 'phone_number'}

    for x in set(sl_map.keys()) - {'w', 'i'}:
        if x in opt_set:
            items_map[sl_map[x]] = ''

    if 'w' in opt_set:
        return tomdb_delete(items_map, target_item[1], org_dic, des_website=True)
    elif 'i' in opt_set:
        return tomdb_delete(items_map, target_item[1], org_dic, des_id=True)
    else:
        return tomdb_delete(items_map, target_item[1], org_dic)
