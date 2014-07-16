# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import json, re
from rakutenscrapy.items import RakutenItemReview

class RakutenSpider(CrawlSpider):
    name = 'review'
    allowed_domains = ['http://product.rakuten.co.jp']

    # read data from jsonline file
    data = []
    f = open('link.jl')
    for line in f:
        data.append(json.loads(line))
    f.close()

    start_urls = []
    for d in data:
        start_urls.append(d['link'])

    def parse(self, response):
        sel = Selector(response)
        match = sel.xpath('//div[@class="revTxt"]')

        for m in match:
            item = RakutenItemReview()
            if len(sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()) >= 1:
                item['genre'] = sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()[0]
            if len(m.xpath('.//text()').extract()) >= 1:
                item['review'] = m.xpath('.//text()').extract()[0]
            yield item
