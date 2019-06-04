# -*- coding: utf-8 -*-
import unittest
import requests
import hashlib
from time import time


class SecAddEventTest(unittest.TestCase):
    """添加发布会（带数字签名）"""

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_add_event/'
        self.api_key = "&guest-manager"
        self.client_time = str(time()).split('.')[0]

        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes)
        self.sign_md5 = md5.hexdigest()

    def test_add_event1_request_error(self):
        """请求方法错误"""
        r = requests.get(self.base_url)
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'request error')

    def test_add_event2_sign_null(self):
        """签名为空"""
        payload = {
            'eid': 1,
            'name': '小米k发布会',
            'limit': 1000,
            'address': '北京',
            'start_time': '2019-04-02 12:00:00',
            'time': '',
            'sign': '',
        }
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user sign null')

    def test_add_event3_timeout(self):
        """请求超时"""
        now_time = str(int(self.client_time) - 60)
        payload = {
            'eid': 1,
            'name': '小米k发布会',
            'limit': 1000,
            'address': '北京',
            'start_time': '2019-04-02 12:00:00',
            'time': now_time,
            'sign': 'abc',
        }
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10013)
        self.assertEqual(result['message'], 'user sign timeout')

    def test_add_event4_sign_error(self):
        """签名错误"""
        payload = {
            'eid': 1,
            'name': '小米k发布会',
            'limit': 1000,
            'address': '北京',
            'start_time': '2019-04-02 12:00:00',
            'time': self.client_time,
            'sign': 'abc',
        }
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10014)
        self.assertEqual(result['message'], 'user sign error')

    def test_add_event5_success(self):
        """添加成功"""
        payload = {
            'eid': 21,
            'name': '小米k发布会',
            'limit': 1000,
            'address': '北京',
            'start_time': '2019-04-02 12:00:00',
            'time': self.client_time,
            'sign': self.sign_md5,
        }
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'add event success')

if __name__ == '__main__':
    unittest.main()