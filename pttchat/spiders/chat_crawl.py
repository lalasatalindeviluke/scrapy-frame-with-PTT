import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import PttchatItem
from scrapy.exceptions import CloseSpider

class c_chatSpider(CrawlSpider):
    name = "chat"
    count_page = 1
    start_urls = ['https://www.ptt.cc/bbs/C_Chat/index.html']
    rules = [Rule(LinkExtractor(allow='/C_Chat/index'),
                  callback='parse_filter', follow=True)]
    def parse_filter(self, response):
        domain = "https://www.ptt.cc"
        partials = response.css(".title a::attr(href)").extract()
        for partial in partials:
            yield scrapy.Request(domain + partial, callback=self.parse_detail)

    def parse_detail(self, response):
        item = PttchatItem()
        title = response.xpath("/html/body/div[3]/div[1]/div[3]/span[2]/text()").extract()
        content = response.xpath('//*[@id="main-content"]/text()').extract()
        item["title"] = title
        item["content"] = content
        yield item
        



