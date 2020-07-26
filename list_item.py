from tomdb import *


def operation_list_gen(org_dic, f_list_all=False):
    items = {'website': '',
             'id': '',
             'username': '',
             'password': '',
             'email': '',
             'phone_number': ''}
    search_arr = tomdb_search(items, org_dic)

    for x in search_arr:
        print('website     :', x[0])
        print('id          :', x[1]['id'])
        print('username    :', x[1]['username'])
        if f_list_all:
            print('password    :', x[1]['password'])
            print('email       :', x[1]['email'])
            print('phone number:', x[1]['phone_number'])
        print('')
    return True


def operation_list(args, org_dic):
    return operation_list_gen(org_dic)


def operation_list_all(args, org_dic):
    return operation_list_gen(org_dic, True)
