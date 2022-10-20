# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from turtle import title
import scrapy


class BonjourbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Product(scrapy.Item):
    title = scrapy.Field()
    # 'body meta[itemprop=description]::attr(content)'
    product_code = scrapy.Field()
    # 'body meta[itemprop=url]::attr(content)'
    sku = scrapy.Field()
    # 'body meta[itemprop=sku]::attr(content)'
    manufacturer = scrapy.Field()
    # 'body meta[itemprop=manufacturer]::attr(content)'
    price = scrapy.Field()
    # 'body meta[itemprop=price]::attr(content)'
    image_link = scrapy.Field()
    # 'body meta[itemprop=image]::attr(content)'
    discount = scrapy.Field()
    brand = scrapy.Field()
    full_price = scrapy.Field()
    # product_code or sku or hashlib.md5(product_code + sku).hexdigest ???
    hash = scrapy.Field()
