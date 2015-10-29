# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

roles = {
    "user": ["user.admin", "user.normal"],
    "bloguser": ["bloguser.admin", "bloguser.normal"]
}


def make_role_validater(roles):
    def validater(v):
        if v in roles:
            return (True, v)
        else:
            return (False, None)

    return validater

role_validaters = {"role_%s" % u: make_role_validater(r) for u, r in roles.items()}
