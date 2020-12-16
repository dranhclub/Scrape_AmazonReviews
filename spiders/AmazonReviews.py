# -*- coding: utf-8 -*-

# Importing Scrapy Library
import scrapy

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
        name = data.css('.a-profile-name')

        #Get the Review Title
        title = data.css('.review-title')

        # Get the Ratings
        star_rating = data.css('.review-rating')

        # Get the users Comments
        comments = data.css('.review-text')
        count = 0

        # combining the results
        for review in star_rating:
            yield{'Name': ''.join(name[count].xpath(".//text()").extract()),
                  'Title': (''.join(title[count].xpath(".//text()").extract())).strip(),
                  'Rating': ''.join(review.xpath('.//text()').extract()),
                  'Comment': (''.join(comments[count].xpath(".//text()").extract())).strip()
                  }
            count = count+1
