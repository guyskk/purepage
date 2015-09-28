from app import app

if __name__ == '__main__':
    # app.config.from_envvar('app.')
    app.run(host="0.0.0.0", debug=True)
