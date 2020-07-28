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


from .tomdb import *
from .console_io import *


def operation_delete(args, org_dic):
    opt_set = option_make_set(args.delete, r'[wiupen]')
    if len(opt_set) == 0:
        print('operation_delete: -d arguments not valid')
        return False
    elif 'w' in opt_set and 'i' in opt_set:
        print('operation_delete: -d conflict options: w and i')
        return False

    items_map = {}
    for x in input_func_map.keys():
        items_map[x] = input_gen(getattr(args, x), f_check=False)
    search_arr = tomdb_search(items_map, org_dic)
    if not search_arr:
        print('operation_delete: specify item not found')
        return False

    target_item = input_select(search_arr)
    if not target_item:
        print('operation_delete: quit select')
        return False

    for x in items_map.keys():
        items_map[x] = ''

    items_map['website'] = target_item[0]
    for x in input_func_map.keys():
        if x == 'website':
            continue
        items_map[x] = target_item[1][x]

    sl_map = {'u': 'username',
              'p': 'password',
              'e': 'email',
              'n': 'phone_number'}

    for x in set(sl_map.keys()):
        if x in opt_set:
            items_map[sl_map[x]] = ''

    if 'w' in opt_set:
        return tomdb_delete(items_map, target_item[1], org_dic, des_website=True)
    elif 'i' in opt_set:
        return tomdb_delete(items_map, target_item[1], org_dic, des_id=True)
    else:
        return tomdb_delete(items_map, target_item[1], org_dic)
