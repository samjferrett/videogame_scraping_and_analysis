from pathlib import Path
import scrapy
from datetime import datetime
import pandas as pd
import numpy as np

class MetaSpider(scrapy.Spider):
    '''
    Class to scrape metacritic videogame data
    '''
    name = "meta"
    #pages to start scrape
    start_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&view=detailed&page={page}'
                  for page in range(201)]
    
    def parse(self, response):
        '''
        Function to scrape game details
        '''
        #retrieve dates and change format to datetime
        dates = response.css('div.clamp-details > span:nth-child(2)::text').getall()
        dates = list(map(lambda date: datetime.strptime(date, "%B %d, %Y"), dates))

        #get all subsequent links to scrape game genres
        genre_links = response.css('a.title::attr(href)').getall()

        #game name, platform, date, user score, metascore
        name = response.css('a.title h3::text').getall()
        platform = list(map(lambda x: x.strip(), response.css('div.platform span.data::text').getall()))
        date = dates
        user_score = response.css('div.clamp-userscore div.metascore_w::text').getall()
        metascore = response.css('div.clamp-score-wrap div.metascore_w::text').getall()

        #loop to retrieve game genre and yield results 
        for name,platform,date,user_score,metascore,link in zip(name,platform,date,user_score,metascore,genre_links):
            data_dict = {'name':name,
                'platform':platform,
                'date': date,
                'user_score': user_score,
                'metascore': metascore}
            yield response.follow(link, self.extra_parse, 
                                  meta = data_dict)

    def extra_parse(self, response):
        '''
        Function to scrape game genres and number of ratings
        '''
        data_dict = {i:response.meta[i] for i in ['name','platform','date','user_score','metascore']}
        genres = response.css('li.product_genre span.data::text').getall()
        data_dict['genre'] = ', '.join(genres)
        try:
            ratings = response.css("div.side_details span.count a::text").get().replace(" Ratings",'')
        except:
            ratings = np.nan
        data_dict['no_ratings'] = ratings

        try:
            critic_ratings = response.css("div.main_details span.count a span::text").get().strip()
        except:
            critic_ratings = np.nan
        data_dict['no_reviews'] = critic_ratings

        return data_dict



