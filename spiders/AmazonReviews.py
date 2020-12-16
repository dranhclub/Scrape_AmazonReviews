# -*- coding: utf-8 -*-

# Importing Scrapy Library
import scrapy
import time
import re

asin_list = [
    'B083KVM9VW',
    'B0777XQ4S8',
    'B07894S727',
    'B07NVRXTGG',
    'B07XSCBSN5',
    'B07R586J37',
    'B006A1PGDE',
    'B00BYH6C1E',
    'B08FB7W3GF',
    'B08B1BFRNX',
    'B07GDKFH9V',
    'B08G1CT5R8',
    'B08PJTV7RY',
    'B0773S1Z9Q',
    'B07BF25F9S',
    'B07H5VTHJV'
]

# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):

    # Spider name
    name = 'amazon_reviews'

    # Domain names to scrape
    allowed_domains = ['amazon.in']

    myBaseUrl = "https://www.amazon.com/product-reviews/B084D89DBF/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="

    start_urls = []

    # Creating list of urls to be scraped by appending page number a the end of base url
    for asin in asin_list:
        for i in range(1, 5):
            start_urls.append(
                f'https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={i}')

    # Defining a Scrapy parser
    def parse(self, response):
        #Get the Review List
        data = response.css('#cm_cr-review_list')

        #Get the Name
        names = data.css('.a-profile-name')

        dates = data.css('.review-date')

        #Get the Review Title
        titles = data.css('.review-title')

        # Get the Ratings
        star_ratings = data.css('.review-rating')

        # Get the users Comments
        comments = data.css('.review-text')

        votes = data.css('.cr-vote-text')

        count = 0

        # combining the results
        for review in star_ratings:
            # time.sleep(0.5)

            name = ''.join(names[count].xpath(".//text()").extract())
            title = (''.join(titles[count].xpath(".//text()").extract())).strip()
            rating = ''.join(review.xpath('.//text()').extract())
            comment = (''.join(comments[count].xpath(".//text()").extract())).strip()
            vote = ''.join(votes[count].xpath(".//text()").extract())

            yield{
                "overall": float(rating[0:3]),
                "vote": 1 if vote[0:3] == "One" else int(re.findall("\d+", vote)[0]),
                "verified": False,
                # "reviewTime": "05 3, 2011",
                # "reviewerID": "A2UEO5XR3598GI",
                # "asin": "B0000530HU",
                # "style": {
                #     "Size:": " 7.0 oz",
                #     "Flavor:": " Classic Ice Blue"
                # },
                "reviewerName": name,
                "reviewText": comment,
                "summary": title,
                # "unixReviewTime": 1304380800
            }

            count = count+1


# scrapy runspider ./spiders/AmazonReviews.py -o output.json