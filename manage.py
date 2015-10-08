# coding:utf-8

if __name__ == '__main__':
    # import os
    # os.environ['KKBLOG_CONFIG'] = 'config/kkblog_config.cfg'
    from kkblog import create_app
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
