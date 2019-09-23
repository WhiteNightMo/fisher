"""
    Created by xukai on 2019/5/29
"""

from app import create_app

# 实例化Flask对象
app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
