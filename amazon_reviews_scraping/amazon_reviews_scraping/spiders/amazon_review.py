# -*- coding: utf-8 -*-
import scrapy
import numpy as np
import pandas as pd
from collections import OrderedDict


class AmazonReviewSpider(scrapy.Spider):
    name = 'amazon_review'
    allowed_domains = ['amazon.com']

    # Here you need to input an asin (Amazon Standard Identification Number)
    # The scraping in base on it. You can find it in the url of the page of your product.
    asin = ['B07N4GKMH8']
    myBaseUrl = "https://www.amazon.com/product-reviews/" + asin[0] + "/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls = []
    # Creating list of urls to be scraped by appending page number a the end of base url
    for j in range(1, 500):
        start_urls.append(myBaseUrl + str(j))

    # Defining a Scrapy parser
    def parse(self, response):
        data = response.css('#cm_cr-review_list')

        # Collecting product star ratings
        star_rating = data.css('.review-rating')

        # Collecting user reviews
        comments = data.css('.review-text')
        count = 0

        # review_list = []
        # stars_list = []
        # Combining the results
        # for review in star_rating:
        #     list.append(''.join(review.xpath('.//text()').extract()))
        #     review_list.append(''.join(comments[count].xpath(".//text()").extract()))
        #     count = count + 1
        # df = pd.DataFrame(OrderedDict({'Stars': np.array(stars_list), 'Reviews': np.array(review_list)}))
        # df.to_csv('reviews.csv', index=False)
        for review in star_rating:
            yield {'stars': ''.join(review.xpath('.//text()').extract()),
               'comment': ''.join(comments[count].xpath(".//text()").extract())
               }
            count = count + 1
