# -*- coding: utf-8 -*-
class GetEventList():
    base_url = 'http://127.0.0.1:8000/api/sec_get_event_list/'
    data = {
        'auth_null':          (10011, 'user auth null'),
        'auth_fail':          (10012, 'user auth fail'),
        'param_err':          (10021, 'paramter error'),
        'result_empty':       (10022, 'query result is empty'),
        'success':            (200, 'success'),
    }

import selenium

if __name__ == '__main__':
    a = id(GetEventList().base_url)
    b = id(GetEventList().base_url)
    print(a, b)