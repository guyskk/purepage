from purepage import create_app
try:
    import config_product as config
except:
    config = None
app = create_app(config)
