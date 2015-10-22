# coding:utf-8

from kkblog import create_app

if __name__ == '__main__':
    import os
    os.environ['KKBLOG_CONFIG'] = os.path.abspath('kkblog_config.py')

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
