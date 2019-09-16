# -*- coding: utf-8 -*-
import scrapy
import urllib
from Mukespider.CourseItems import CourseItem
class MukewangSpider(scrapy.Spider):
    name = 'mukewang'
    allowed_domains = ['imooc.com']
    start_urls = ['http://imooc.com/course/list?page=2']

    def parse(self, response):
        item = CourseItem()
        for box in response.xpath('.//div[@class="course-card-container"]'):
            item['url'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
            item['title'] = box.xpath('.//h3/text()').extract()[0]
            item['student'] = box.xpath('.//div[@class="course-card-info"]/span[2]/text()').extract()[0]
            item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()

            if len(box.xpath('.//div[@class="course-label"]/label/text()').extract())==1:

                item['catycray'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0]

            elif len(box.xpath('.//div[@class="course-label"]/label/text()').extract())==2:
                item['catycray'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0]+' '+ box.xpath('.//div[@class="course-label"]/label/text()').extract()[1]
            elif len(box.xpath('.//div[@class="course-label"]/label/text()').extract())==3:
                item['catycray'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0]+' '+box.xpath('.//div[@class="course-label"]/label/text()').extract()[1]+' '+ box.xpath('.//div[@class="course-label"]/label/text()').extract()[2]
            else :
                item['catycray'] = ''

            print(item['title'])
            yield scrapy.Request(item['url'], callback=self.parseNest, meta=item)

    def parseNest(self, response):

        item = response.meta
        item['degree'] = response.xpath('//div[contains(@class,"static-item l")]/span[contains(@class,"meta-value")]/text()').extract()[0]
        item['hour'] = response.xpath('//div[contains(@class,"static-item l")]/span[contains(@class,"meta-value")]/text()').extract()[1]
        if len(response.xpath('//div[@class="static-item l score-btn"]/span[@class="meta-value"]/text()').extract())==0:
            item['score'] = ''
        else:
            item['score'] = response.xpath('//div[@class="static-item l score-btn"]/span[@class="meta-value"]/text()').extract()

        yield item

        for x in xrange(3, 31):
            page = 'http://www.imooc.com/course/list?page=' + str(x)
            yield scrapy.Request(page, callback=self.parse)