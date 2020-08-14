import logging

import scrapy
from scrapy.crawler import CrawlerProcess


logger = logging.getLogger('labelsbaselogger')


def increment_search_page(url):
    """
        Increment the search. results page number
    """
    if "=" not in url:
        # page DNE on the first search
        return url + "page=2"
    else:
        (url_prefix, page_number) = url.split("=")
        return "{0}{1}".format(url_prefix, int(page_number) + 1)


class LabelsBaseSpider(scrapy.Spider):
    
    name = "labelsbase"
    start_urls = ['https://labelsbase.net/search?']

    def parse(self, response):
        
        label_urls = response.xpath('//div[@class="label-item-description"]/div/a/@href').getall()
        logger.info('Parsing %s', response.url)
        next_page = increment_search_page(self.url)
        if next_page is not None:
            yield response.follow(next_page, self.parse)


def main():

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(LabelsBaseSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    main()
