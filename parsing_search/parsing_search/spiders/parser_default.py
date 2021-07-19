import scrapy
from parsing_search.user_agents import USER_AAGENTS
import random
import time
import re
from parsing_search.items import UrlItem


class QuotesSpider(scrapy.Spider):
    name = "parsing_search"
    count = 1
    url_set = set()

    pattern = re.compile(r'p=[0-9]{1,2}')

    def start_requests(self):
        
        urls = [
            'https://yandex.ru/search/?text=%D0%A0%D1%8E%D0%BA%D0%B7%D0%B0%D0%BA%20%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&lr=1',
            'https://yandex.ru/search/?text=%D0%BF%D0%BE%D1%81%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D0%B1%D0%B5%D0%BB%D1%8C%D0%B5%20%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C%20%D0%B2%20%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B5&lr=1',
            'https://yandex.ru/search/?text=%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82%20%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%D1%8B%20%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%BD%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4&lr=1',
            'https://yandex.ru/search/?text=%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B0%20%D0%BC%D0%B5%D1%85%D0%B0%20&lr=1',
            'https://yandex.ru/search/?text=%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B8%D0%B2%D0%BD%D0%B0%D1%8F%20%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0&lr=1',
            'https://yandex.ru/search/?text=%D1%82%D1%83%D1%80%D0%B8%D1%81%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D1%84%D0%B8%D1%80%D0%BC%D1%8B%20%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8&lr=1',
            'https://yandex.ru/search/?text=%D1%81%D0%B0%D0%B9%D1%82%D1%8B%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%B9%20%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8&lr=1',


        ]

        for url in urls:
            self.count += 1
            user_ag = random.choice(USER_AAGENTS)
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 headers={'User-Agent': user_ag},
                                 cb_kwargs={'main_request': url, 'page': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,\
                                                                          15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                                            'count': self.count}
                                 )

    def parse(self, response, **kwargs) -> object:
        if response.status == 200 and len(response.cb_kwargs.get("page")) != 0:

            if self.pattern.search(response.url):
                if len(response.cb_kwargs.get("page")) > 1:
                    index = random.randrange(0, len(response.cb_kwargs.get("page")))
                else:
                    index = 0

                new_url = re.sub(self.pattern, f'p={response.cb_kwargs.get("page").pop(index)}', response.url)

            else:
                index = random.randrange(0, 24)
                new_url = response.url + f'&p={response.cb_kwargs.get("page").pop(index)}'

            user_ag = random.choice(USER_AAGENTS)
            yield scrapy.Request(url=new_url,
                                 callback=self.parse,
                                 headers={'User-Agent': user_ag},
                                 meta={'dont_merge_cookies': True},
                                 cb_kwargs=response.cb_kwargs
                                 )

        else:
            yield UrlItem(
                url=set()
            )




