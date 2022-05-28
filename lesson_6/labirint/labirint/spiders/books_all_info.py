import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksAllInfoSpider(CrawlSpider):
    name = 'books_all_info'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=
                           "//div[@class='pagination-next']/a[contains(text(), 'Следующая')]"),
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=
                           "//div[@data-title='Все в жанре «Книги»']/div[@class='card-column card-column_gutter col-xs-6 col-sm-3 col-md-1-5 col-xl-2']/div/div[@class='product-cover']/a"), follow=True, callback='parse_item')
    )


    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath(
            "//div[@id='product-about']/h2/text()").get().replace('Аннотация к книге ', '').replace("\"", '')
        # item['img'] = response.xpath("//div[@id='product-image']/img[@class='book-img-cover']/@data-original").get()
        item['rate'] = response.xpath("//div[@id='rate']/text()").get()
        item['authors'] = response.xpath("//div[@class='product-description']//div[@class='authors']/a/text()").get()
        if response.xpath("//span[@class='buying-price-val-number']/text()").get() is not None:
            item['price'] = response.xpath("//span[@class='buying-price-val-number']/text()").get()
            item['currency'] = response.xpath("//span[@class='buying-pricenew-val-currency']/text()").get()
            item['price_old'] = None
            item['price_new'] = None
        else:
            if response.xpath("//span[@class='buying-priceold-val-number']/text()").get() is not None:
                item['price'] = None
                item['price_old'] = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
                item['price_new'] = response.xpath(
                    "//span[@class='buying-pricenew-val-number']/text()").get()
                item['currency'] = response.xpath(
                    "//span[@class='buying-pricenew-val-currency']/text()").get()
            else:
                item['price_old'] = None
                item['price_new'] = None
                item['currency'] = None
                item['price_old'] = 'Товара нет в наличии'
        item['annotation'] = response.xpath("//div[@id='product-about']/p/text()").get()
        item['location'] = response.xpath("//div[@class='prodtitle-availibility rang-available']/span/text()").get()
        item['publisher'] = response.xpath("//div[@class='publisher']/a/text()").get()
        item['series'] = response.xpath("//div[@class='series']/a/text()").get()
        item['isbn'] = response.xpath("//div[@class='isbn']/text()").get()
        item['articul'] = response.xpath("//div[@class='articul']/text()").get()
        return item
