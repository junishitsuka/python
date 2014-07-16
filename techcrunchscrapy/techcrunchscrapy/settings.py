# -*- coding: utf-8 -*-

# Scrapy settings for techcrunchscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'techcrunchscrapy'

SPIDER_MODULES = ['techcrunchscrapy.spiders']
NEWSPIDER_MODULE = 'techcrunchscrapy.spiders'

DOWNLOAD_DELAY = 3 # sleep間隔
ROBOTSTXT_OBEY = True # robots.txtに従うかどうか

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'techcrunchscrapy (+http://www.yourdomain.com)'
