import scrapy

# селекторы главной страницы
category_pages_links = "a.js517::attr(href)"

#  селекторы страницы категории
product_links_css = 'a[class~=productNameLink]::attr(href)'
pagination_links_css = '#PaginationRoot a::attr(href)'

# скидка без акции = len(response.css('div[itemprop=offers] > div > div')) > 2
# процент скидки без акции = response.css('div[itemprop=offers] > div > div')[1].css('div > div > div > div::text')[1].get()
# цена без скидки без акции = response.css('div[itemprop=offers] > div > div')[1].css('div > s::text')[0].get()

# скидка с акцией = response.css('a[href*=promotion]').get() != None
# процент скидки с акцией = response.css('a[href*=promotion]')[1].css('div::text')[1].get()
# цена без скидки с акцией = response.css('a[href*=promotion]')[1].css('s::text')[0].get()
# акция с подарком без скидки = response.css('a[href*=promotion]')[0].css('a::attr(href)')


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

            # скидка с акцией без подарка
            with_promotion_without_prize = len(response.css(
                'a[href*=promotion]')) > 1
            # скидка без акции
            without_promotion = len(response.css(
                'div[itemprop=offers] > div > div')) > 2

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
        discount = get_discount_and_full_price(response)["discount"]
        brand = extr('span[itemprop=brand]::text')
        full_price = get_discount_and_full_price(response)["full_price"]

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
        }

    def parse(self, response):
        # список ссылок на продукт
        product_links = response.css(product_links_css).getall()
        # обход продуктовых ссылок
        yield from response.follow_all(product_links, self.parse_product)

        # # список ссылок пагинации
        pagination_links = [
            link.split('&')[0] for link in response.css(
                '#PaginationRoot a::attr(href)'
            ).getall()
        ]
        # обход ссылок пагинации
        yield from response.follow_all(pagination_links, self.parse)
