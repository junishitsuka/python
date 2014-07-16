# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import json, re
from rakutenscrapy.items import RakutenItemDetail

class RakutenSpider(CrawlSpider):
    name = 'item'
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

        item = RakutenItemDetail()
        item['link'] = response.url
        if len(sel.xpath('//h1/text()').extract()) >= 1:
            item['title'] = sel.xpath('//h1/text()').extract()[0]
        if len(sel.xpath('//span[@class="price"]/text()').extract()) >= 1:
            item['price'] = sel.xpath('//span[@class="price"]/text()').extract()[0]
        if len(sel.xpath('//span[@class="maker"]/a/text()').extract()) >= 1:
            item['maker'] = sel.xpath('//span[@class="maker"]/a/text()').extract()[0]
        if len(sel.xpath('//span[@class="reviewRating"]/text()').extract()) >= 1:
            item['review'] = sel.xpath('//span[@class="reviewRating"]/text()').extract()[0]
        if len(sel.xpath('//span[@class="reviewNumber"]/a/span/text()').extract()) >= 1:
            item['review_count'] = sel.xpath('//span[@class="reviewNumber"]/a/span/text()').extract()[0]
        # item['jan'] = re.search(r"JAN:\d*", sel.xpath('//div[@class="quickInfo"]').extract()[0]).group().split(':')[1]
        if len(sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()) >= 1:
            item['genre'] = sel.xpath('//div[@id="pankuzu"]/ul/li/div/span/span/span/span/span/a/span/text()').extract()[0]

        if len(sel.xpath('//div[@id="contents"]/script/text()').extract()) >= 1:
            js = sel.xpath('//div[@id="contents"]/script/text()').extract()[0]
            js = re.sub('\s', '', js)
            js = re.sub("'", '', js)
            dsc = re.search(r'height=100%;document.getElementById\(onoff1\).innerHTML="(.*)";document.getElementById\(onoff2\)', js)
            dsc = re.search(r'"(.*)"', dsc.group())
            item['description'] = dsc.group()

        yield item
