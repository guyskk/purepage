# coding:utf-8

from kkblog import create_app
app = create_app()

if __name__ == '__main__':
    # import os
    # os.environ['KKBLOG_CONFIG'] = 'config/kkblog_config.cfg'
    app.run(host="0.0.0.0", use_debugger=True, debug=True)
