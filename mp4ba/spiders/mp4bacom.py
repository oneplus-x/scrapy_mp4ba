# -*- coding: utf-8 -*-
import scrapy
from mp4ba.items import Mp4BaItem


class Mp4bacomSpider(scrapy.Spider):
    name = "mp4bacom"
    allowed_domains = ["mp4ba.com"]
    start_urls = (
        'http://www.mp4ba.com/index.php?page=1',
    )

    def parse(self, response):
        for info in response.xpath('//tbody[@id="data_list"]/tr[@class]'):
            item = Mp4BaItem()
            item['moive_name'] = info.xpath('td[@style="text-align:left;"]/a/text()').extract()[0].lstrip()
            item['moive_url'] = "magnet:?xt=urn:btih:"+ info.xpath('td[@style="text-align:left;"]/a/@href').extract()[0].split("?")[-1]+r"&tr=http://bt.mp4ba.com:2710/announce"
            item['moive_type'] = info.xpath('td[2]/a[1]/text()').extract()[0]
            yield item

        next_page = response.xpath('//div[@class="pages clear"]/a[@class="nextprev"][last()]/@href')  # next page
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

