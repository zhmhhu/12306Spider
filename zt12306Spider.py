from asyncio import  get_event_loop
from pyppeteer import launch
from random import randint
from main import main
from verification_code import slide_list


class Zt12306Spider:
    def __init__(self,username,password):
        self.width, self.height = 1366, 768
        self.username = username
        self.password = password
        get_event_loop().run_until_complete(self.init())
        get_event_loop().run_until_complete(self.login())

    async def init(self):
        self.browser = await launch(headless=False,
                                   args=['--disable-infobars', f'--window-size={self.width},{self.height}', '--no-sandbox'])
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': self.width, 'height': self.height})
        await self.page.goto('https://kyfw.12306.cn/otn/resources/login.html')
        await self.page.evaluate('()=>{Object.defineProperties(navigator,{webdriver:{get:()=>false}})}')

    async def login(self):
        await self.page.click('.login-hd-account')
        await self.page.type('#J-userName', self.username, {'delay': randint(60, 120)})  # 账号
        await self.page.type('#J-password', self.password, {'delay': randint(100, 151)})  # 密码

        # 验证码
        code = await self.page.waitForSelector('#J-loginImg')  # 通过css selector定位验证码元素
        # 验证码截图
        await code.screenshot({'path': 'captcha.jpg'})
        # 获取验证码坐标
        box = await code.boundingBox()

        # 获取验证码
        result = ''
        text, check = main('captcha.jpg')
        for t in text:
           for pos, l in check:
               if t == l:
                   result += str(pos) + ','
        resultNums = result[:-1]
        print(resultNums)  # 字符串
        if len(resultNums) > 0:
            resList = resultNums.split(',')

            await self.page.waitFor(1 * 1000)
            for res in resList:
               if int(res) < 5:
                   await self.page.mouse.click(box['x'] + 37 * (2 * int(res) - 1), box['y'] + 70)
                   await self.page.waitFor(randint(567, 3456))
               else:
                   await self.page.mouse.click(box['x'] + 37 * (2 * int(res) - 9), box['y'] + 150)
                   await self.page.waitFor(randint(567, 3456))
            await self.page.waitFor(1 * 1000)
            await self.page.click('#J-login')

            slider = await self.page.Jeval('#login_slide_box', 'node => node.style')  # 是否有滑块
            if slider:
                print('出现滑块')
                await self.page.waitFor('.btn_slide')
                await self.slide_move('.btn_slide')
            # await self.page.waitFor(150 * 1000)
            await self.page.waitForNavigation()
            await self.page.waitFor(3 * 1000)
            await self.page.click('.modal-ft >a')
            await self.page.goto('https://kyfw.12306.cn/otn/view/information.html') #跳转到个人信息页面
            await self.page.waitFor(5 * 1000)

        else:
            print('验证码自动识别失败，请重试')

    async def slide_move(self, slide_id):
        await self.page.hover(slide_id)
        # await self.page.evaluate('document.querySelector("'+slide_id+'").hover()')
        await self.page.mouse.down()
        slides = slide_list(300)
        x = self.page.mouse._x
        for distance in slides:
            x += distance
            await self.page.mouse.move(x, 0, )
        await self.page.mouse.up()


if __name__ == '__main__':
    username = 'alex603'
    password = 'zhaomin12306'
    Zt12306Spider(username, password)
