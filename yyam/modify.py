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
