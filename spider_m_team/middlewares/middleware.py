from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice


ua_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
        ]

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 15
dcap["phantomjs.page.settings.loadImages"] = False
dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)




class JSMiddleware(object):
    def process_request(self, request, spider):
        if spider.name=="m_Team_Spider":
            print("PhantomJS is starting...")
            driver=webdriver.PhantomJS(executable_path=r"./phantomjs/bin/phantomjs",
                                       desired_capabilities=dcap)
            url = str(request.url)
            driver.get(url)
            print(type(request.meta))

            driver.add_cookie()
            content=driver.page_source
            with open('PantonJS.html','w') as f:
                f.write(content)

            driver.close()
            return HtmlResponse(request.url, body=content, encoding='utf-8', request=request )

