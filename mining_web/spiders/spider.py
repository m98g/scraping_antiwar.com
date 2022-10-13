from sys import path
import os 

path.append(os.getcwd())

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from scrapy.settings import Settings
import mining_web.settings as my_settings
from scrapy.loader import ItemLoader
from mining_web.items import MiningWebItem




class antiwarSpider(scrapy.Spider):
    name = "antiwar"

    allowed_domains = [
        'news.antiwar.com'
    ]
    start_urls = [
        'https://news.antiwar.com/2020/12/31/uk-judge-to-give-decision-on-assange-extradition-on-monday/',
    ]

    def parse(self, response):
        it = ItemLoader(item=MiningWebItem(), response=response)
        print(response)
         
        # very crude data has to be cleaned
        it.add_xpath('Title', "//div[@id='primary']//header[@class='entry-header']")
        it.add_xpath('Author', "//div[@id='primary']//footer[@class='entry-footer']//span[@class='byline']//a")
        it.add_xpath('Date', "//div[@id='primary']//footer[@class='entry-footer']//span[@class='posted-on']/a")
        it.add_xpath('Text', "//div[@id='primary']//div[@class='entry-content']/*")
        yield it.load_item()
        ### The yielded items are somehow also processes by the items and itempipeline. ###
        # for title in response.css('header.entry-header'):
            #  yield {'Title': [title.css('h1.entry-title::text').get()]}

        # for ref in response.css('footer.entry-footer'):
            #yield {
            #    'By': ref.css('a.url::text').get(),
            #    'Date': ref.css('time.entry-date::text').get()
            #    }

        # for text in response.css('div.entry-content'):
          #  yield {'Text': text.css('p::text').getall()}

        #for link in response.css('div.nav-previous'):
         #   yield {'Prev': link.css('a::attr(href)').get()}

        # give a specific date to stop downloading when its hit
        for ref in response.css('footer.entry-footer'):
            x = ref.css('time.entry-date::text').get()
            if '2019' in x:
                print(x)
                # get the url and store it in a txt
                with open('last_url.txt', 'w') as l:
                    l.write(str(response.request.url))
                    print('--- Wrote last url to file. ---')
                raise CloseSpider("--- Target Date hit. ---")

        next_page = response.css('nav.post-navigation a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(antiwarSpider)
    process.start()
