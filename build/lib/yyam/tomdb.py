import re
import datetime

from .tomrw import *


def tomdb_gen(website='',
              order_num='1',
              identify='',
              username='',
              password='',
              email='',
              phone_number='',
              used_username=[],
              used_password=[],
              used_email=[],
              used_phone_number=[],
              modify_time='',
              modify_count=0):

    new_dic = {website: {}}

    curr_dic = new_dic[website]
    curr_dic[str(order_num)] = {}
    curr_dic = curr_dic[str(order_num)]
    curr_dic['username'] = username
    curr_dic['password'] = password
    curr_dic['id'] = identify
    curr_dic['email'] = email
    curr_dic['phone_number'] = phone_number

    curr_dic['history'] = {}
    curr_dic['history']['used_username'] = used_username
    curr_dic['history']['used_password'] = used_password
    curr_dic['history']['used_email'] = used_email
    curr_dic['history']['used_phone_number'] = used_phone_number

    curr_dic['info'] = {}
    curr_dic['info']['modify_time'] = modify_time
    curr_dic['info']['modify_count'] = modify_count

    curr_dic['etc'] = {}

    return new_dic


def tomdb_history_add(sub_dic, history_dic={}):
    now_time = datetime.datetime.now()
    sub_dic['info']['modify_time'] = now_time
    sub_dic['info']['modify_count'] += 1

    sl_map = {'username': 'used_username',
              'password': 'used_password',
              'email': 'used_email',
              'phone_number': 'used_phone_number'}
    if history_dic == {}:
        pass
    else:
        for name in history_dic.keys():
            if history_dic[name] != '':
                temp_arr = [history_dic[name], str(now_time)]
                sub_dic['history'][sl_map[name]].append(temp_arr)
    
    return True


def tomdb_search(items, org_dic):
    org_arr = []
    for web_key in org_dic.keys():
        order_set = set(org_dic[web_key].keys()) - {'total_number'}
        for order_key in order_set:
            org_arr.append([web_key, org_dic[web_key][order_key]])

    count_arr = [i - i for i in range(0, len(org_arr))]
    if items['website'] == '':
        pass
    else:
        for i in range(0, len(org_arr)):
            if re.match(items['website'], org_arr[i][0]):
                pass
            else:
                count_arr[i] += 1

    for name in set(items.keys()) - {'website'}:
        if items[name] == '':
            continue
        else:
            for i in range(0, len(org_arr)):
                if re.match(items[name], org_arr[i][1][name]):
                    pass
                else:
                    count_arr[i] += 1

    dst_arr = []
    for i in range(0, len(count_arr)):
        if count_arr[i] == 0:
            dst_arr.append(org_arr[i])

    return dst_arr


def tomdb_new(items, org_dic):
    if items['website'] not in org_dic.keys():
        order = 1
    else:
        order = org_dic[items['website']]['total_number'] + 1
        exist_order = set(org_dic[items['website']].keys()) - {'total_number'}
        for x in exist_order:
            if items['id'] == org_dic[items['website']][x]['id']:
                print('operation_add_new: tomdb_new: id already exists')
                return False

    new_dic = tomdb_gen(website=items['website'],
                        order_num=order,
                        identify=items['id'],
                        username=items['username'],
                        password=items['password'],
                        email=items['email'],
                        phone_number=items['phone_number'])

    if items['website'] not in org_dic.keys():
        new_dic[items['website']]['total_number'] = 1
        org_dic[items['website']] = new_dic[items['website']]
    else:
        org_dic[items['website']]['total_number'] = order
        org_dic[items['website']][str(order)] = new_dic[items['website']][str(order)]

    return tomdb_history_add(org_dic[items['website']][str(order)])


def tomdb_add(items, sub_dic):
    for name in set(items.keys()) - {'website', 'id'}:
        if items[name] != '':
            if sub_dic[name] == '':
                sub_dic[name] = items[name]
            else:
                print('operation_add_add: tomdb_add: at least one item already exist')
                return False

    return tomdb_history_add(sub_dic)


def tomdb_update(items, sub_dic):
    history_dic = {'username': '',
                   'password': '',
                   'email': '',
                   'phone_number': ''}
    for name in set(items.keys()) - {'website', 'id'}:
        if items[name] != '':
            history_dic[name] = sub_dic[name]
            sub_dic[name] = items[name]

    return tomdb_history_add(sub_dic, history_dic)


def tomdb_delete(items, sub_dic, org_dic, des_website=False, des_id=False):
    if des_website is True:
        del org_dic[items['website']]
        return True
    elif des_id is True:
        for x in set(org_dic[items['website']].keys()) - {'total_number'}:
            if org_dic[items['website']][x] is sub_dic:
                del org_dic[items['website']][x]
                break
        if org_dic[items['website']]['total_number'] == 1:
            del org_dic[items['website']]
        else:
            org_dic[items['website']]['total_number'] -= 1
            total_num = org_dic[items['website']]['total_number']
            sub_item_arr = []
            for x in set(org_dic[items['website']].keys()) - {'total_number'}:
                sub_item_arr.append(org_dic[items['website']][x])
                del org_dic[items['website']][x]
            for i in range(1, total_num + 1):
                org_dic[items['website']][str(i)] = sub_item_arr[i - 1]
        return True
    else:
        history_dic = {'username': '',
                       'password': '',
                       'email': '',
                       'phone_number': ''}
        for x in history_dic.keys():
            if items[x] == '':
                history_dic[x] = sub_dic[x]
                sub_dic[x] = ''
        return tomdb_history_add(sub_dic, history_dic)


def tomdb_read(dir_path):
    f = open(dir_path, 'r', encoding='utf-8')
    in_str = f.read()
    org_dic = tom_parse(in_str)
    f.close()
    return org_dic


def tomdb_write(dir_path, org_dic):
    out_str = tom_dump(org_dic)
    f = open(dir_path, 'w', encoding='utf-8')
    print(out_str, file=f)
    f.close()
    return True
