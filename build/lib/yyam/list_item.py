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
from .console_io import input_gen


def operation_list_gen(org_dic, f_list_all=False):
    items = {'website': '',
             'id': '',
             'username': '',
             'password': '',
             'email': '',
             'phone_number': ''}

    search_arr = tomdb_search(items, org_dic)
    if not search_arr:
        print('operation_list_gen: no item exist')
        return True

    if f_list_all:
        print('make sure there is nobody around you')
        validation_name = input_gen(None, '.+', "author's name for validation")
        if validation_name in ['yy', 'include-yy']:
            pass
        else:
            print('name not correct')
            return False

    for x in search_arr:
        print('website     :', x[0])
        print('id          :', x[1]['id'])
        print('username    :', x[1]['username'])
        if f_list_all:
            print('password    :', x[1]['password'])
            print('email       :', x[1]['email'])
            print('phone number:', x[1]['phone_number'])
        print('')

    print('the number of website is', len(org_dic.keys()))
    print('the number of account is', len(ssearch_arr))
    return True


def operation_list(args, org_dic):
    return operation_list_gen(org_dic)


def operation_list_all(args, org_dic):
    return operation_list_gen(org_dic, True)
