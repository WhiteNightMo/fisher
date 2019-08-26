"""
    Created by xukai on 2019/5/30
"""

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        """
        ger请求
        :param url: url
        :param return_json: 是否以json格式返回
        :return: json|string
        """
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
