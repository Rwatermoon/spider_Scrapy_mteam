from scrapy.selector import Selector,HtmlXPathSelector
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from scrapy.http import response
from spider_m_team.items import SpiderMTeamItem
import re



# class JSMiddleware(object):
#     def process_request(self, request, spider):
#         print(spider.name)
#         if spider.name=="LJspider":
#             print("PhantomJS is starting...")
#             driver=webdriver.PhantomJS(executable_path="spider_m_team/phantomjs/bin/phantomjs",
#                                        desired_capabilities=dcap)
#             url = str(request.url)
#             driver.get(url)
#             content=driver.page_source
#             driver.close()
#             return HtmlResponse(request.url, body=content, encoding='utf-8', request=request, )



with open('./response_html/199636.html') as f:
    # partten=re.compile(r'^(\d{3})')
    # print(f.read())
    # print(partten.match(f.read()).groups())
    driver = webdriver.PhantomJS(executable_path="./phantomjs/bin/phantomjs")

    driver.get('./response_html/199636.html')
    content = driver.page_source
    driver.close()
    #
    #
    av_item=Selector(text=content)
    # # html=Selector(text=content)
    # print(html.xpath('//*[@id="top"]/text()').extract())

    record_item = SpiderMTeamItem()
    url = "https://tp.m-team.cc/details.php?id=199804&hit=1"
    record_item['item_id'] = url[url.find('id=') + 3:url.find('&hit=1')]
    record_item['item_title'] = av_item.xpath('//*[@id="top"]/text()').extract()
    record_item['item_actor'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[1]/td[2]/span/@title').extract()
    record_item['item_tags'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[4]/td[2]/a/b/text()').extract()

    record_item['item_publish_time'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[1]/td[2]/span/@title').extract()
    record_item['item_size'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[1]').extract()
    record_item['item_category'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[2]').extract()
    record_item['item_encoding'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[3]').extract()
    record_item['item_resolution'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[4]').extract()
    record_item['item_dealwith'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[5]').extract()

    record_item['item_seed_IPV4HTTPS'] = av_item.xpath(
        '//*[@id="outer"]/table[2]/tbody/tr[8]/td[2]/b[2]/a[1]/@href').extract()
    record_item['item_upload_count'] = av_item.xpath('//*[@id="peercount"]/b[1]/text()').extract()
    record_item['item_download_count'] = av_item.xpath('//*[@id="peercount"]/b[2]/text()').extract()
    record_item['item_finish_count'] = av_item.xpath(
        '//*[@id="outer"]/table[2]/tbody/tr[13]/td[2]/table/tbody/tr/td[3]/a/b/text()').extract()

    record_item['item_cover_url'] = av_item.xpath('//*[@id="kdescr"]/img/@src').extract()
    record_item['item_dmm_type'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[11]/td[2]/div[1]').extract()
    record_item['item_dmm_text'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[11]/td[2]/div[2]').extract()
    record_item['item_dmm_pic'] = av_item.xpath(
        '//*[@id="outer"]/table[2]/tbody/tr[11]/td[2]/div[3]/img/@src').extract()

    for item in record_item['item_tags']:
        print(item)
    # for key,value in record_item._values.items():
    #     print(key,value)
    # self.save_response_body(response, record_item['item_id'])

    # xpath parese for list
    # for item in html.xpath('//table[@class="torrents"]/tbody/tr'):
    #     # print(item.extract())
    #
    #     print('title: ',item.xpath('td[2]/table//tr/td[2]/a/b/text()').extract())
    #     print('publish_time: ', item.xpath('td[4]/span/@title').extract())
    #     print('size: ', item.xpath('td[5]/text()').extract())
    #     print('up: ', item.xpath('td[6]/b/a/text()').extract())
    #     print('down: ', item.xpath('td[7]/b/a/text()').extract())
    #     print('finish: ', item.xpath('td[8]/a/b/text()').extract())
    #     print('url: ', item.xpath('td[2]/table//tr/td[2]/a/@href').extract())
    # print(html.xpath('//*[@id="outer"]/table[2]/tbody/tr/td/p/a[1]/@href').extract())



