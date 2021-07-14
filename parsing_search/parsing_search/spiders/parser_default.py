import scrapy


class QuotesSpider(scrapy.Spider):
    name = "parsing_search"
    url_search = 'https://yandex.ru/search/?text=%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%81%D1%82%D0%B2%D0%B0%20%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8&lr=0'
    page = 2
    url_list =[]

    def start_requests(self):
        
        urls = [
            self.url_search                        
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            
            links = response.css('a.Link.Link_theme_normal.OrganicTitle-Link')
            for link in links:
                self.url_list.append(link.attrib['href'])
            
            new_url = self.url_search + f'&p={self.page}'
            yield scrapy.Request(url=new_url, callback=self.parse)
            print('==========================================================================================================')
            self.page +=1
        else:
            print(self.url_list)
        