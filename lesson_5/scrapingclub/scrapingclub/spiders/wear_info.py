import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WearInfoSpider(CrawlSpider):
    name = 'wear_info'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//nav/ul/li[@class='page-item']/a[contains(text(), 'Next')]"),
             follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='card']/a"), follow=True, callback='parse_item')
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath("//div[@class='card-body']/h3/text()").get()
        item['price'] = response.xpath("//div[@class='card-body']/h4/text()").get()
        item['description'] = response.xpath("//div[@class='card-body']/p/text()").get()
        item['image'] = response.urljoin(response.xpath("//div[@class='card mt-4 my-4']/img/@src").get())
        return item
