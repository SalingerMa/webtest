# -*- coding: utf-8 -*-
import unittest
import requests


class GetEventListTest(unittest.TestCase):
    """查询发布会信息（带用户认证）"""
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_get_event_list/"

    def test_get_event_list1_auth_null(self):
        """auht为空"""
        r = requests.get(self.base_url, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'user auth null')

    def test_get_event_list2_auth_error(self):
        """auth错误"""
        auth_user = ('abc', '123')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user auth fail')

    def test_get_event_list3_eid_null(self):
        """eid参数为空"""
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_list4_result_empty(self):
        """根据eid查询结果为空"""
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1000})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_list5_eid_success(self):
        """根据eid查询结果成功"""
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], u'红米Pro发布会')
        self.assertEqual(result['data']['address'], u'北京会展中心')


if __name__ == '__main__':
    unittest.main()