from . import web


@web.route('/')
def index():
    return 'This is web index page'


@web.route('/personal')
def personal_center():
    pass
