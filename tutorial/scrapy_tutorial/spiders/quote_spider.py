import scrapy


class QuoteSpiderSpider(scrapy.Spider):
    name = "quote_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                # quote
                'text_re': quote.re(r"\"text\">(.*)</span>\n"), # using regex
                'text.css': quote.css('span.text::text').get(), # using css

                'text_xpath': quote.xpath('span[@class="text"]/text()').get() # using xpath
                
            }

# Run the spider
# scrapy crawl quote_spider

# Save the output to a file
# scrapy crawl quote_spider -o quotes.json


# shell
# scrapy shell "http://quotes.toscrape.com/"
# response.css('title::text').get()
# response.css('div.quote').getall()
# response.css('div.quote').get()
# response.css('div.quote span.text::text').getall()
# response.css('div.quote span.text::text').get()
# response.css('div.quote span.text::text').extract()
# response.css('div.quote span.text::text').extract_first()
# response.css('div.quote span.text::text').extract_first().strip()
# response.css('div.quote span.text::text').extract_first().strip().split()
# response.css('div.quote span.text::text').extract_first().strip().split()[0]
# response.css('div.quote span.text::text').extract_first().strip().split()[0].lower()
# response.css('div.quote span.text::text').extract_first().strip().split()[0].lower().capitalize()
# response.css('div.quote span.text::text').extract_first().strip().split()[0].lower().capitalize().replace('a', 'A')
# response.css('div.quote span.text::text').extract_first().strip().split()[0].lower().capitalize().replace('a', 'A').replace('b', 'B')
