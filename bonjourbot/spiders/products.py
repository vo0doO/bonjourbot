import scrapy
import hashlib
# селекторы главной страницы
category_pages_links = "a.js517::attr(href)"

#  селекторы страницы категории
product_links_css = 'a[class~=productNameLink]::attr(href)'
pagination_links_css = '#PaginationRoot a::attr(href)'


class ProductsSpider(scrapy.Spider):
    name = 'products'

    start_urls = [
        # 'https://bonjour-dv.ru/category/1',
        'https://bonjour-dv.ru/category/26',  # бытовая техника 185 товаров
        'https://bonjour-dv.ru/category/258',  # товары для животных 79 товаров
        'https://bonjour-dv.ru/category/179',  # подарки и сувениры 202 товаров
        # 'https://bonjour-dv.ru/category/318',
        # 'https://bonjour-dv.ru/category/53',
    ]

    def parse_product(self, response):

        def extr(q):
            text = response.css(q).get()
            if text == None:
                return "Отсутствует"
            else:
                return text.strip()

        title = extr('body meta[itemprop=description]::attr(content)')
        product_code = extr(
            'body meta[itemprop=url]::attr(content)'
        ).split("/")[-1]
        sku = extr('body meta[itemprop=sku]::attr(content)')
        manufacturer = extr('body meta[itemprop=manufacturer]::attr(content)')
        price = extr('body meta[itemprop=price]::attr(content)')
        image_link = extr(
            'body meta[itemprop=image]::attr(content)'
        ).split("?")[0]
        discount = ""
        brand = ""
        full_price = ""
        hash_string = title+sku+price
        hash = hashlib.md5(hash_string.encode("utf-8")).hexdigest()

        yield {
            'title': title,
            'product_code': product_code,
            'sku': sku,
            'manufacturer': manufacturer,
            'price': price,
            'image_link': image_link,
            'discount': discount,
            'brand': brand,
            "full_price": full_price,
            "hash": hash,
        }

    def parse(self, response):
        # список ссылок на продукт
        product_links = response.css(product_links_css).getall()
        # обход продуктовых ссылок
        yield from response.follow_all(product_links, self.parse_product)

        # # список ссылок или одна ссылка пагинации
        pagination_links = [
            link.split('&')[0] for link in response.css(
                '#PaginationRoot a::attr(href)'
            ).getall()
        ]
        # обход ссылок пагинации
        yield from response.follow_all(pagination_links, self.parse)
