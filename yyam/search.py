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
