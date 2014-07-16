# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from techcrunchscrapy.items import TechcrunchscrapyItem
from scrapy.selector import HtmlXPathSelector
import sys

class TechcrunchSpider(CrawlSpider):
    name = 'url'
    allowed_domains = ['http://techcrunch.com']
    start_urls = []
    for i in range(1, 15):
        start_urls.append("http://techcrunch.com/sitemap.xml?yyyy=2014&mm=07&dd=%02d" % i)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        match = hxs.select('//loc/text()')
        print match

        for m in match:
            item = TechcrunchscrapyItem()
            item['link'] = m.extract()
            yield item
        # item['title'] = sel.xpath('//h1/text()').extract()[0]
        # item['body'] = sel.xpath('//div[@class="article-entry text"]/text()').extract()[0]
        # item['time'] = sel.xpath('//div[@class="byLine"]/time/text()').extract()[0]
        # item['author'] = sel.xpath('//div[@class="byLine"]/a/text()').extract()[0]
        # item['html'] = sel.xpath('/html').extract()[0]
        # yield item
