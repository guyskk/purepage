# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import StringIO
import string
from flask import current_app, make_response, session
from flask_restaction import Resource

CHARS = set(string.ascii_letters + string.digits)
CHARS = CHARS - set('Il1o0')

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
        font = current_app.config["CAPTCHA_FONT"]
        captcha_img = create_captcha(text, font)
        buf = StringIO.StringIO()
        captcha_img.save(buf, 'JPEG', quality=70)
        buf_str = buf.getvalue()
        response = make_response(buf_str)
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
