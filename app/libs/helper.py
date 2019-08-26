"""
    Created by xukai on 2019/5/30
"""


def is_isbn_or_key(word):
    """
    判断搜索字段是isbn还是普通关键字
    :param word: 搜索字段
    :return: isbn|key
    """
    isbn_or_key = 'key'
    # isbn13: 13个0-9的数字组成
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    # isbn10: 10个0-9的数字组成，其中含有一些'-'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
