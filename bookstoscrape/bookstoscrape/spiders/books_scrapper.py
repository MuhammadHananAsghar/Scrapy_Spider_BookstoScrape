import scrapy

class BooksSpider(scrapy.Spider):
    name = "booksscrapper"

    def start_requests(self):
        urls = ['https://books.toscrape.com/catalogue/page-1.html,'
                'https://books.toscrape.com/catalogue/page-2.html',
                'https://books.toscrape.com/catalogue/page-3.html',
                'https://books.toscrape.com/catalogue/page-4.html',
                'https://books.toscrape.com/catalogue/page-5.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        articles = response.xpath('//article[@class="product_pod"]');
        for article in articles:
            link = article.xpath(".//a")
            cleaned_url = response.url.split("page")[0]
            book_link = cleaned_url+link.xpath("@href").extract()[0]
            book_image = cleaned_url+link.xpath(".//img").xpath("@src").extract()[0]
            book_name = link.xpath(".//img").xpath("@alt").extract()[0].strip()
            book_price = article.xpath(".//p[@class='price_color']/text()").extract()[0].strip();
            book_in_stock = article.xpath(".//p[@class='instock availability']/text()").extract()[-1].strip()
            yield scrapy.Request(url=book_link, callback=self.parse_book_page)

    def parse_book_page(self, response, **kwargs):
        main_url = "https://books.toscrape.com/"
        product_page = response.xpath("//article[@class='product_page']");
        book_cover = product_page.xpath(".//div[@class='carousel-inner']").xpath(".//img").xpath("@src").extract()[0];
        book_cover = main_url+book_cover.split("../")[-1]
        prod_div = product_page.xpath(".//div[@class='col-sm-6 product_main']");
        book_name = prod_div.xpath(".//h1/text()").extract()[0].strip();
        book_price = prod_div.xpath(".//p[@class='price_color']/text()").extract()[0].strip();
        book_avail = prod_div.xpath(".//p[@class='instock availability']/text()").extract()[-1].strip();
        book_description = product_page.xpath('//*[@id="content_inner"]/article/p/text()').extract()[0].strip().replace(" ...more", "");
        yield {
            "Name": book_name,
            "Cover": book_cover,
            "Price": book_price,
            "Availability": book_avail,
            "Description": book_description
        }
