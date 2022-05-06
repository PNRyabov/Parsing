import scrapy


class WearToScrapeSpider(scrapy.Spider):
    name = 'wear_to_scrape'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic']

    def parse(self, response):
        article = response.xpath("//div[@class='card']")
        for articl in article:
            yield{
                'title': articl.xpath(".//div[@class='card-body']/h4/a/text()").get(),
                'image': response.urljoin(articl.xpath(".//a/img/@src").get()),
                'price': articl.xpath(".//div[@class='card-body']/h5/text()").get(),
            }
        next_page = response.xpath("//nav/ul/li[@class='page-item']/a[contains(text(), 'Next')]/@href").get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)