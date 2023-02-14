# videogame_scraping_and_analysis
Project involving data scraping using scrapy from metacritic.com to create a dataset and analysis of data using python

## metacritic_scrape

Code to run scrapy on metacritic.com to gater the data "metacritic_data_130223.json"

To run enter the following from metacritic_scrape/metacritic_scrape:

    scrapy crawl meta -O metacritic_data_130223.json

This will use metacritic_scrape/spiders/meta_spider.py to scrape the required data

## metacritic_scrape_beautifulsoup

Alternative that uses beautiful soup. Note this data does not include number of ratings stats and is typically slower than the scrapy version