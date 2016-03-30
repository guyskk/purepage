# coding=utf-8
"""
无状态验证码
0. 服务端先配置一个密钥KEY
1. 客户端请求验证码TOKEN
   服务端生成一个随机字符串TEXT，再生成一个SALT，用KEY和SALT对TEXT进行加密
   加密后的TEXT和SALT拼接到一起，作为TOKEN返回给客户端
2. 客户端请求验证码图片，携带验证码TOKEN
   服务端根据KEY和TOKEN中的SALT，解密出TEXT，用这个TEXT生成一幅图片
3. 客户端发送业务请求，携带验证码TOKEN和用户输入的CODE
   服务端根据KEY和TOKEN中的SALT，解密出TEXT，和CODE比对
"""
from __future__ import unicode_literals, absolute_import, print_function
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import StringIO
import string
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES
from werkzeug.security import gen_salt
from datetime import datetime, timedelta
from flask import current_app, make_response, url_for
from flask_restaction import Resource


def encrypt(text, key):
    """加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数.
    这里密钥salt 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    text: byte string
    """
    salt = gen_salt(16)
    cryptor = AES.new(key, mode=AES.MODE_CBC, IV=salt)
    length = 16
    count = len(text)
    add = length - (count % length)
    text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return "%s$%s" % (b2a_hex(ciphertext), salt)


def decrypt(text, key):
    """解密后，用strip()去掉补足的空格
    text: byte string
    """
    if text.count('$') < 1:
        return False
    token, salt = text.split('$', 1)
    cryptor = AES.new(key, mode=AES.MODE_CBC, IV=salt)
    plain_text = cryptor.decrypt(a2b_hex(token))
    return plain_text.rstrip('\0')


def check_captcha(token, text, key):
    try:
        text2 = decrypt(token, key)
        return text.lower() == text2.lower()
    except:
        return False


def create_captcha(text, font_type, height=30, mode="RGB",
                   point_chance=15, twisty=15):
    """
    height: 图片的高度，宽度为 int(height * 0.5 * len(text))
    mode: 图片模式，默认为RGB
    font_type: 验证码字体
    point_chance: 干扰点出现的概率，大小范围[0, 100]
    twisty: 扭曲程度，大小范围[0, 100]
    """

    def random_color(mid=125):
        a = random.randint(0, 255)
        b = random.randint(0, 255)

        # 让其中一个颜色更重
        if abs(a - b) < mid:
            if min(a, b) > mid:
                c = random.randint(0, mid)
            else:
                c = random.randint(max(a, b), 255)
        else:
            c = random.randint(0, 255)
        color = [a, b, c]
        random.shuffle(color)
        return tuple(color)

    length = len(text)
    bg_color = (255, 255, 255)
    fg_color = random_color()
    fg_color = (fg_color[0] * 2, fg_color[1] / 2, fg_color[2] / 2)
    width = int(height * 0.5 * length)
    # 创建图形
    img = Image.new(mode, (width, height), bg_color)
    # 创建画笔
    draw = ImageDraw.Draw(img)

    def create_points():
        """绘制干扰点"""
        # 大小限制在[0, 100]
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=random_color())

    def create_text():
        """绘制验证码字符"""
        # 生成给定长度的字符串
        font_size = int(height * 0.7)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(text)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  text, font=font, fill=fg_color)

    def create_lines():
        """绘制干扰线"""
        begin = (random.randint(0, width / length),
                 random.randint(height / 5, height - height / 5))
        end = (random.randint(width - width / length, width),
               random.randint(height / 5, height - height / 5))
        draw.line([begin, end], fill=random_color(), width=1)

    def create_twisty(img):
        # 图形扭曲参数
        random_twisty = lambda: float(random.randint(0, twisty / 5))
        params = [1 - random_twisty() / 1000, 0, 0, 0,
                  1 - random_twisty() / 100, 0.001,
                  random_twisty() / 5000,
                  random_twisty() / 5000
                  ]
        # 或者用下面的参数
        # params = [1 - float(random.randint(1, 2)) / 100,
        #           0,
        #           0,
        #           0,
        #           1 - float(random.randint(1, twisty)) / 100,
        #           float(random.randint(1, 2)) / 500,
        #           0.001,
        #           float(random.randint(1, 2)) / 500
        #           ]
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
        img = img.transform((width, height), Image.PERSPECTIVE, params)  # 创建扭曲
        return img

    create_points()
    create_text()
    create_lines()
    img = create_twisty(img)
    return img


def check(token, text):
    key = current_app.config["CAPTCHA_KEY"]
    return check_captcha(token, text, key)


class Captcha(Resource):
    """图形验证码"""

    schema_inputs = {
        "get": None,
        "get_show": {
            "token": "unicode&required"
        },
        "get_check": {
            "token": "unicode&required",
            "text": "unicode&required"
        }
    }
    schema_outputs = {
        "get": {
            "token": "unicode&required",
            "url": "unicode&required"
        },
        "get_show": None,
        "get_check": {
            "token": "unicode&required",
            "text": "unicode&required",
            "success": "bool&required"
        },
    }

    def get(self):
        """获取一个验证码链接"""
        key = current_app.config["CAPTCHA_KEY"]
        text = ''.join(random.sample(CHARS, 4))
        token = encrypt(text, key)
        token = token.encode("ascii")
        return {
            "token": token,
            "url": "%s?token=%s" % (url_for("api.captcha@show"), token)
        }

    def get_show(self, token):
        """显示验证码"""
        key = current_app.config["CAPTCHA_KEY"]
        token = token.encode("ascii")
        try:
            text = decrypt(token, key)
            assert len(text) == 4, "解密失败"
        except:
            return "token无效", 404
        font = current_app.config["CAPTCHA_FONT"]
        captcha_img = create_captcha(text, font)
        buf = StringIO.StringIO()
        captcha_img.save(buf, 'JPEG', quality=70)

        buf_str = buf.getvalue()

        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/jpeg'
        return response

    def get_check(self, token, text):
        """查看验证码是否正确"""
        return {
            "token": token,
            "text": text,
            "success": check(token, text)
        }
