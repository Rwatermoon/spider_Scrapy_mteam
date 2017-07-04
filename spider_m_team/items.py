# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderMTeamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_id=scrapy.Field()
    item_title = scrapy.Field()
    item_actor=scrapy.Field()
    item_tags=scrapy.Field()

    item_publish_time=scrapy.Field()
    item_size=scrapy.Field()
    item_category=scrapy.Field()
    item_encoding=scrapy.Field()
    item_resolution=scrapy.Field()
    item_dealwith=scrapy.Field()

    item_seed_IPV4HTTPS=scrapy.Field()
    item_upload_count=scrapy.Field()
    item_download_count=scrapy.Field()
    item_finish_count=scrapy.Field()

    item_cover_url=scrapy.Field()
    item_dmm_type=scrapy.Field()
    item_dmm_text = scrapy.Field()
    item_dmm_pic = scrapy.Field()
