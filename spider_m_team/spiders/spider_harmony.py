"""
Author:Rwatermoon
Date:2017/6/9
Description:
        crawl av item from m-Team form
        make the life harmony!!!!!
"""
import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest,HtmlResponse
from spider_m_team.items import SpiderMTeamItem

class mTeamSpider(CrawlSpider):
    name = 'm_Team_Spider'
    allow_domain = ['https://tp.m-team.cc']
    start_urls=['https://tp.m-team.cc/adult.php']
    rules = (
        Rule(LinkExtractor(allow=(r'details.php\?id=\d+')), callback='parse_detial_item'),
    )

    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2",
    "Cache - Control": "max - age = 0",
    "Connection": "keep-alive",
    "Content - Length": "35",
    "Content-Type":" application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }

    def start_requests(self):
        return [Request("https://tp.m-team.cc/adult.php", meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        print('Preparing login')
        return [FormRequest.from_response(response,
                            url='https://tp.m-team.cc/takelogin.php',
                            meta = {'cookiejar' : response.meta['cookiejar'],
                                    },
                            headers = self.headers,
                            formdata = {
                            'username': settings['FROM_USERNAME'],
                            'password': settings['FROM_PASSWORD'],
                            },
                            callback = self.after_login,
                            dont_filter=True
                            )]

    def after_login(self, response) :
        if 'Rwatermoon' in str(response.body):print('Success')
        else:print('login fails')
        with open('filename.html', 'wb') as f:
            f.write(response.body)
        for url in self.start_urls :
            yield scrapy.Request(url,meta = {'cookiejar': response.meta['cookiejar']},
                                 headers=self.headers,dont_filter=True)


    def save_response_body(self,response,item_id):
        if response.url is None:return
        filename='./response_html/'+item_id+'.html'
        with open(filename,'wb') as f:
            f.write(response.body)

    def parse_detial_item(self, response):
        print(response.url,len(response.body))


        av_item=Selector(response)
        print(av_item.xpath('//*[@id="top"]/text()').extract())
        record_item = SpiderMTeamItem()
        url=str(response.url)
        record_item['item_id']=url[url.find('id=')+3:url.find('&hit=1')]
        record_item['item_title']=av_item.xpath('//*[@id="top"]/text()').extract()
        record_item['item_actor'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[1]/td[2]/span/@title').extract()
        record_item['item_tags'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[4]/td[2]/a/b/text()').extract()

        record_item['item_publish_time'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[1]/td[2]/span/@title').extract()
        record_item['item_size'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[1]').extract()
        record_item['item_category'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[2]').extract()
        record_item['item_encoding'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[3]').extract()
        record_item['item_resolution'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[4]').extract()
        record_item['item_dealwith'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[5]/td[2]/text()[5]').extract()

        record_item['item_seed_IPV4HTTPS'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[8]/td[2]/b[2]/a[1]/@href').extract()
        record_item['item_upload_count'] =av_item.xpath('//*[@id="peercount"]/b[1]/text()').extract()
        record_item['item_download_count'] =av_item.xpath('//*[@id="peercount"]/b[2]/text()').extract()
        record_item['item_finish_count'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[13]/td[2]/table/tbody/tr/td[3]/a/b/text()').extract()

        record_item['item_cover_url'] =av_item.xpath('//*[@id="kdescr"]/img/@src').extract()
        record_item['item_dmm_type'] =av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[11]/td[2]/div[1]').extract()
        record_item['item_dmm_text'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[11]/td[2]/div[2]').extract()
        record_item['item_dmm_pic'] = av_item.xpath('//*[@id="outer"]/table[2]/tbody/tr[11]/td[2]/div[3]/img/@src').extract()

        for key,value in record_item._values.items():print(key,':',value)
        self.save_response_body(response, record_item['item_id'])

        yield record_item

    def parse_list_item(self,response):
        # with open('filename.html', 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file filename')
        print(response.url)
        with open('filename_adult.html', 'wb') as f:
            f.write(response.body)
        publish_item=Selector(response)
        record_item=SpiderMTeamItem()
        for table_item in publish_item.xpath('//*[@id="form_torrent"]'):
            print(table_item.xpath('//tr/td/table//tr/td/a/b/text()').extract(),
                  table_item.xpath('//*[@id="form_torrent"]/table//tr[3]/td[5]/text()').extract())
        # for item in item_title:print(item)
        # print(item_title)
        # return item_title
        # for torrent_item in response.xpath('//*[@id="form_torrent"]/table/tbody/tr[9]/td[2]'):
        #     yield {
        #     'title':torrent_item.extract(),}
        # item_publish_date = scrapy.Field()
        # item_detial_url = scrapy.Field()
        # item_size = scrapy.Field()
        # item_size_unit = scrapy.Field()
        # item_upload_count = scrapy.Field()
        # item_download_count = scrapy.Field()
        # item_finish_count = scrapy.Field()
    #
    # def request_question(self, request):
    #     return Request(request.url, meta={'cookiejar': 1}, headers=self.headers, callback=self.parse_detial_item)

    def _requests_to_follow(self, response):

        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            links=[l for l in links if l.text is '']
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = Request(url=link.url,callback=self._response_downloaded)
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])
                yield rule.process_request(r)

print('ok')
