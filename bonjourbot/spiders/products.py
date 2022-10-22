import scrapy


class ProductsSpider(scrapy.Spider):
    name = 'products'

    start_urls = [
        'https://bonjour-dv.ru/category/1',  #  белье и текстиль 1062
        'https://bonjour-dv.ru/category/26',  # бытовая техника 185 товаров
        'https://bonjour-dv.ru/category/258',  # товары для животных 79 товаров
        'https://bonjour-dv.ru/category/186',  # товары для детей 1077 товаров
    ]

    def parse_product(self, response):

        def get_discount_and_full_price(response):

            with_promotion_without_prize = len(response.css('a[href*=promotion]')) > 1
            without_promotion = len(response.css('div[itemprop=offers] > div > div')) > 2

            if with_promotion_without_prize:
                return {
                    "discount": response.css('a[href*=promotion]')[1].css('div::text')[1].get(),
                    "full_price": response.css('a[href*=promotion]')[1].css('s::text')[0].get()
                }
            elif without_promotion:
                return {
                    "discount": response.css('div[itemprop=offers] > div > div')[1].css('div > div > div > div::text')[1].get(),
                    "full_price": response.css('div[itemprop=offers] > div > div')[1].css('div > s::text')[0].get()
                }
            else:
                return {
                    "discount": "Отсутствует",
                    "full_price": "Отсутствует"
                }

        def extr(q: str) -> str:

            text = response.css(q).get()

            if text == None:
                return "Отсутствует"
            else:
                return text.strip()

        yield {
            'title': extr('body meta[itemprop=description]::attr(content)'),
            'product_code': extr('body meta[itemprop=url]::attr(content)').split("/")[-1],
            'sku': extr('body meta[itemprop=sku]::attr(content)'),
            'manufacturer': extr('body meta[itemprop=manufacturer]::attr(content)'),
            'price': extr('body meta[itemprop=price]::attr(content)'),
            'image_link': extr('body meta[itemprop=image]::attr(content)').split("?")[0],
            'discount': get_discount_and_full_price(response)["discount"],
            'brand': extr('span[itemprop=brand]::text'),
            "full_price": get_discount_and_full_price(response)["full_price"],
        }

    def parse(self, response):

        product_links = response.css('a[class~=productNameLink]::attr(href)').getall()
        yield from response.follow_all(product_links, self.parse_product)

        pagination_links = [link.split('&')[0] for link in response.css('#PaginationRoot a::attr(href)').getall()]
        yield from response.follow_all(pagination_links, self.parse)
