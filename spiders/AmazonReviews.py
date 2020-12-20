# -*- coding: utf-8 -*-

# Importing Scrapy Library
import scrapy
import time
import re
import json
import pandas
import os

# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
    # Spider name
    name = 'amazon_reviews'
    # Add user_agent to avoid 503 error
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    # Asin (Amazon Standard Identification Number) list
    asin_list = []

    # Get asin list
    dir_path = 'data/asin_list/'
    for filename in os.listdir(dir_path):
        df = pandas.read_csv(dir_path + filename)
        asins = df['asin'].values.tolist()
        asin_list += asins

    # Test
    # asin_list = ['B000X7ST9Y']

    # Domain names to scrape
    allowed_domains = ['amazon.in']

    start_urls = []

    # Creating list of urls to be scraped by appending page number a the end of base url
    for asin in asin_list:
        for i in range(1, 5):
            start_urls.append(
                f'https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={i}&sortBy=recent')

    # Defining a Scrapy parser
    def parse(self, response):
        asin = response.request.url[39:49]
        # asin = response.request.url

        #Get the Review List
        div_review_list = response.css('#cm_cr-review_list')
        div_reviews = div_review_list.css('.review')
        
        for div_review in div_reviews:
            name = div_review.css("span.a-profile-name::text").get()
            title = (''.join(div_review.css(".review-title").xpath(".//text()").extract())).strip()
            rating = div_review.css(".review-rating ::text").get()
            # date = div_review.css(".review-date::text").re(r'(January|February|Match|April|May|June|July|August|October|September|November|December) \d*, \d*')[0]
            date = div_review.css(".review-date::text").re("on (.*)")[0]
            text = (''.join(div_review.css(".review-text-content").xpath(".//text()").extract())).strip()
            vote = div_review.css(".cr-vote-text::text").get()
            verified = div_review.css('span[data-hook="avp-badge"]::text').get()

            # Only get review from 2019
            if (int(date[-4:]) < 2019): 
                continue

            yield{
                "overall": float(rating[0:3]),
                "vote": 0 if not vote else 1 if vote[0:3] == "One" else int(re.findall("\d+", vote)[0]),
                "verified": verified == "Verified Purchase",
                "reviewTime": date,
                # "reviewerID": "A2UEO5XR3598GI",
                "asin": asin,
                # "style": {
                #     "Size:": " 7.0 oz",
                #     "Flavor:": " Classic Ice Blue"
                # },
                "reviewerName": name,
                "reviewText": text,
                "summary": title,
                # "unixReviewTime": 1304380800
            }