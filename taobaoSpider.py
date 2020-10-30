from asyncio import sleep, get_event_loop
from pyppeteer import launch
from random import random
from re import compile, S
import asyncio


class TaoBaoSpider:
    def __init__(self):
        self.width, self.height = 1500, 800
        get_event_loop().run_until_complete(self.init())
        get_event_loop().run_until_complete(self.login())
        get_event_loop().run_until_complete(self.search())
        get_event_loop().run_until_complete(self.crawl())

    async def init(self):
        # noinspection PyAttributeOutsideInit
        self.browser = await launch(
            headless=False,
            args=["--disable-infobars", f"--window-size={self.width},{self.height}"],
        )
        # noinspection PyAttributeOutsideInit
        self.page = await self.browser.newPage()
        await self.page.setViewport({"width": self.width, "height": self.height})
        await self.page.goto(
            "https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/"
        )
        await self.page.evaluate(
            "()=>{Object.defineProperties(navigator,{webdriver:{get:()=>false}})}"
        )

    async def login(self):
        # await page.goto('https://login.taobao.com/member/login.jhtml')
        # await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        # await page.waitForSelector('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static', {'timeout': 3000})
        # await page.click('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
        await self.page.type("#fm-login-id", "15088499794")  # 账号
        await self.page.type("#fm-login-password", "alex_312")  # 密码
        # slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
        # if slider:
        #     print('出现滑块')
        await self.page.click(".password-login")
        await asyncio.sleep(5)

    @property
    def sleep_time(self):
        return 1 + random() * 3

    async def search(self):
        await self.page.click("#q")
        await sleep(self.sleep_time)
        await self.page.keyboard.type("机械革命")
        await sleep(self.sleep_time)
        await self.page.click("#J_TSearchForm > div.search-button > button")
        await sleep(self.sleep_time)

    async def crawl(self):
        pattern = compile(r'<a id=".*?" class="J_ClickStat".*?>(.*?)</a>', S)
        repl_pattern = compile(r"<.*?>|\s+")
        for i in range(5):
            # document.body.clientHeight
            height = await self.page.evaluate("document.body.clientHeight")
            scrolled_height = 0
            a = 1 + random()
            t = 1
            # window.scrollTo(width,height)
            while scrolled_height < height:
                scrolled_height = int(1 / 2 * a * t ** 2)  # x=v0*t+1/2*a*t**2,v0=0
                await self.page.evaluate(f"window.scrollTo(0,{scrolled_height})")
                t += 1
            await sleep(self.sleep_time)
            html = await self.page.content()
            results = pattern.findall(html)
            for result in results:
                result = repl_pattern.sub("", result)
                print(result)
            print()
            await sleep(self.sleep_time)
            await self.page.click(
                "#mainsrp-pager > div > div > div > ul > li.item.next > a"
            )
            await sleep(self.sleep_time)
        await sleep(self.sleep_time)


if __name__ == "__main__":
    TaoBaoSpider()
