# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    company_name = scrapy.Field()
    # job_name = scrapy.Field()
    work_address = scrapy.Field()
    work_experice = scrapy.Field()
    education = scrapy.Field()
    salary = scrapy.Field()

