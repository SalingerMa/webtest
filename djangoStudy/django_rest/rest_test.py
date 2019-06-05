# -*- coding: utf-8 -*-
import unittest
import requests

class UserTest(unittest.TestCase):
    """用户查询测试"""
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/users"
        self.auth = ('admin', 'admin123456')

    def test_user1(self):
        """测试用户admin"""
        r = requests.get(self.base_url+'/1/', auth=self.auth)
        result = r.json()
        print(result)
        self.assertEqual(result['username'], 'admin')

    def test_user2(self):
        r = requests.get(self.base_url + '/2/', auth=self.auth)
        result = r.json()
        print(result)
        self.assertEqual(result['username'], 'jack')

    def test_user3(self):
        r = requests.get(self.base_url + '/3/', auth=self.auth)
        result = r.json()
        print(result)
        self.assertEqual(result['username'], 'tom')

if __name__ == '__main__':
    unittest.main()