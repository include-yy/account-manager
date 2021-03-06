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


from .console_io import *
from .tomdb import *


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
    if not target_item:
        print('operation_add_add: quit select')
        return False

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
