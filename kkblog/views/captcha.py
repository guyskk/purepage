# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import random
import string
from flask import make_response, session
from flask_restaction import Resource
from captcha.image import ImageCaptcha

image = ImageCaptcha(fonts=['kkblog/georgia.ttf'])
CHARS = set(string.ascii_letters + string.digits)
CHARS = CHARS - set('Il1o0')


class Captcha(Resource):
    """图形验证码"""

    schema_inputs = {
        "get": None,
        "get_check": {
            "text": "unicode&required"
        }
    }
    schema_outputs = {
        "get": None,
        "get_check": {
            "text": "unicode&required",
            "success": "bool&required"
        }
    }

    def get(self):
        """显示验证码"""
        text = ''.join(random.sample(CHARS, 4))
        print(text)
        session["captcha_text"] = text
        data = image.generate(text)
        response = make_response(data.getvalue())
        response.headers['Content-Type'] = 'image/jpeg'
        return response

    def get_check(self, text):
        """查看验证码是否正确"""
        session.setdefault("captcha_success", False)
        captcha = session.get("captcha_text")
        success = bool(captcha is not None and captcha.lower() == text.lower())
        session["captcha_success"] = success
        return {
            "text": text,
            "success": success
        }
