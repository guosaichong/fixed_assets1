import random
import string
from PIL import Image, ImageDraw, ImageFont


def gene_text(number):
    """生成随机字符串"""
    source = string.ascii_letters
    return "".join(random.sample(source, number))


def gene_code(size, number, bgcolor, font, fontsize, fontcolor, linecolor):
    """
    生成验证码图片
    :param size: 验证码图片大小。A 2-tuple, containing (width, height) in pixels.
    :param number: 验证码的位数。
    :param bgcolor: 验证码图片的背景色。(255,250,240)
    :param font: 验证码字体。'../static/fonts/simkai.ttf'
    :param fontsize: 验证码字体大小。
    :param fontcolor: 验证码的字体颜色。(255,0,0)
    :param linecolor: 干扰线颜色。(190,190,190)
    :return: An ~PIL.Image.Image object,code string.
    """

    width, height = size
    image = Image.new("RGBA", (width, height), bgcolor)
    font_ttf = ImageFont.truetype(font, fontsize)
    draw = ImageDraw.Draw(image)
    text = gene_text(number)
    font_width, font_height = font_ttf.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font_ttf, fill=fontcolor)
    for i in range(3):
        begin = (random.randint(0, width/2), random.randint(0, height))
        end = (random.randint(width/2, width), random.randint(0, height))
        draw.line([begin, end], fill=linecolor)
    return image,text


if __name__ == "__main__":
    font = '../static/fonts/simkai.ttf'
    gene_code((90, 30), 4, (255, 250, 240), font,
              25, (255, 0, 0), (190, 190, 190))
