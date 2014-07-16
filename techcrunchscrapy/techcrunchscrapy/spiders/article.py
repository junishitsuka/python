# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from techcrunchscrapy.items import TechcrunchscrapyItem
from scrapy.selector import HtmlXPathSelector
import sys, json

class TechcrunchSpider(CrawlSpider):
    name = 'article'
    allowed_domains = ['http://techcrunch.com']

    # read data from jsonline file
    data = []
    f = open('url.jl')
    for line in f:
        data.append(json.loads(line))
    f.close()

    start_urls = []
    for d in data:
        start_urls.append(d['link'])

    def parse(self, response):
        sel = Selector(response)

        item = TechcrunchscrapyItem()
        if len(sel.xpath('//h1/text()').extract()) >= 1:
            item['title'] = sel.xpath('//h1/text()').extract()[0]
        if len(sel.xpath('//div[@class="article-entry text"]/text()').extract()) >= 1:
            item['body'] = sel.xpath('//div[@class="article-entry text"]/text()').extract()[0]
        if len(sel.xpath('//div[@class="byLine"]/time/text()').extract()) >= 1:
            item['time'] = sel.xpath('//div[@class="byLine"]/time/text()').extract()[0]
        if len(sel.xpath('//div[@class="byLine"]/a/text()').extract()) >= 1:
            item['author'] = sel.xpath('//div[@class="byLine"]/a/text()').extract()[0]
        if len(sel.xpath('//html').extract()) >= 1:
            item['html'] = sel.xpath('//html').extract()[0]
        yield item
