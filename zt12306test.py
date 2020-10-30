
from main import main


def crackvcFunc(imagepath):
    """验证码识别函数
    传入图片，返回验证码识别后的结果
    """
    result = ''
    # 打开验证码图片
    # img = Image.open(imagepath)
    text,check = main(imagepath)
    # 识别验证码图片
    # result = IdentifyAPI(img)
    for t in text:
        for pos,l in check:
            if t == l:
                result += str(pos)+','
    # 返回识别结果
    print(result[:-1])
    return result[:-1]


if __name__ == '__main__':
    crackvcFunc('captcha.jpg')


