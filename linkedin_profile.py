# put this file into spiders dir

import json
import scrapy
from ..selenium_request import SeleniumRequest
from bs4 import BeautifulSoup


class LinkedinProfileSpider(scrapy.Spider):
    name = "linkedin_revolut_employees"
    custom_settings = {'DOWNLOADER_MIDDLEWARES': {'scrapers.middlewares.SeleniumMiddleware': 543}}
    base_url = 'https://www.linkedin.com/search/results/people/?heroEntityKey=urn%3Ali%3Aorganization%3A5356541&keywords=revolut&origin=FACETED_SEARCH&pastCompany=%5B%225356541%22%5D&position=0&searchId=e567f82a-beea-4739-a21d-736d1bbe3347&page={}'

    def start_requests(self):
        urls_index_tracker = 1
        first_url = 'https://www.linkedin.com/search/results/people/?heroEntityKey=urn%3Ali%3Aorganization%3A5356541&keywords=revolut&origin=FACETED_SEARCH&pastCompany=%5B%225356541%22%5D&position=0&searchId=e567f82a-beea-4739-a21d-736d1bbe3347&page={}'\
                    .format(1)
        yield SeleniumRequest(url=first_url,
                              headers={'Accept-Language': 'en',
                                       'Content-Language': 'en'},
                              callback=self.parse_response,
                              meta={'urls_index_tracker': urls_index_tracker})

    def parse_response(self, response):
        urls_index_tracker = response.meta['urls_index_tracker']

        profiles_urls = []
        try:
            soup = BeautifulSoup(response.text)
            profile_cards = soup.find_all('li', class_='reusable-search__result-container')
            for profile_card in profile_cards:
                if len(profile_url := profile_card.find_all('a', href=True)) > 0:
                    profiles_urls.extend([url.get('href') for url in profile_url])
        except Exception as err:
            print(err)

        yield {'profiles': profiles_urls}

        urls_index_tracker = urls_index_tracker + 1
        if urls_index_tracker <= 100:
            next_url = self.base_url.format(urls_index_tracker)

            yield SeleniumRequest(url=next_url, callback=self.parse_response,
                                  meta={'urls_index_tracker': urls_index_tracker})
