"""
    Created by xukai on 2019/8/12
"""


class BookViewModel:
    """
    单本book数据模型
    """

    def __init__(self, book):
        """
        对book原数据进行整理
        :param book: 原数据
        """
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author = '、'.join(book['author']) if type(book['author']) == 'dict' else book['author']
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['image']


class BookCollection:
    """
    book集合
    """

    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.keyword = keyword


class _BookViewModel:
    """
    （已废弃）面向过程式写法
    """

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        """
        裁剪book数据
        :param data:
        :return:
        """

        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image'],
        }
        return book
