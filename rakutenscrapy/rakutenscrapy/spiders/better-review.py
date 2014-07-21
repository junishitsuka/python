# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import json, re
from rakutenscrapy.items import RakutenItemReview

class RakutenSpider(CrawlSpider):
    name = 'better-review'
    allowed_domains = ['http://product.rakuten.co.jp']

    # read data from jsonline file
    data = []
    f = open('link.jl')
    for line in f:
        data.append(json.loads(line))
    f.close()

    start_urls = []
    for d in data:
        start_urls.append(d['link'] + '/review/1/')

    def parse(self, response):
        sel = Selector(response)
        match = sel.xpath('//div[@class="revTxt"]')
        title_match = sel.xpath('//div[@class="revTitle"]')

        for m in match:
            item = RakutenItemReview()
            if len(sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()) >= 1:
                item['genre'] = sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()[0]
            if len(m.xpath('.//text()').extract()) >= 1:
                item['review'] = m.xpath('.//text()').extract()[0]
            yield item

        for tm in title_match:
            item = RakutenItemReview()
            if len(sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()) >= 1:
                item['genre'] = sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()[0]
            if len(tm.xpath('.//text()').extract()) >= 1:
                if tm.xpath('.//text()').extract()[0] != '':
                    item['review'] = tm.xpath('.//text()').extract()[0]
                    yield item
