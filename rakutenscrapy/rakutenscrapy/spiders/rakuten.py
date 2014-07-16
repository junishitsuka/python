# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from rakutenscrapy.items import RakutenItem


class RakutenSpider(CrawlSpider):
    name = 'rakuten'
    allowed_domains = ['http://product.rakuten.co.jp']
    start_urls = []
    for i in range(1, 13):
        start_urls.append("http://product.rakuten.co.jp/503169/?p=%d" % i)

    def parse(self, response):
        sel = Selector(response)
        match = sel.xpath('//div[@class="proListItemName"]/table')

        for m in match:
            item = RakutenItem()
            item['title'] = m.xpath('.//a/text()').extract()[0]
            item['link'] = m.xpath('.//a/@href').extract()[0]
            yield item
