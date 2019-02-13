# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapydemo.boss.boss.items import BossItem


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=python&page=1']

    rules = (
        # https://www.zhipin.com/job_detail/?query=python
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'), follow=True),
        # https://www.zhipin.com/job_detail/0fb429ab223517641HV73Nm-EFs~.html?ka=search_list_4
        Rule(LinkExtractor(allow=r'.+/job_detail/.+\.html'), callback='parse_job', follow=False),
    )

    def parse_job(self, response):
        company_name = response.xpath('//a[@ka="job-detail-company"]/text()')[2].get().strip()
        # job_name = response.xpath('//div[@class="name"]/h1/text()').extract_first()
        work_address = response.xpath('//p/text()')[0].get()
        work_experice = response.xpath('//p/text()')[1].get()
        education = response.xpath('//p/text()')[2].get()
        salary = response.xpath('//div[@class="name"]/span/text()').get().strip()
        item = BossItem(company_name=company_name,work_address=work_address, work_experice=work_experice, education=education, salary=salary)
        yield item
