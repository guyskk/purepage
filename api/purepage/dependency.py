from flask_github import GitHub
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.local import LocalProxy

github = GitHub()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)


class Dependency:
    """Dependency"""

d = Dependency()

api = LocalProxy(lambda: d.api)
