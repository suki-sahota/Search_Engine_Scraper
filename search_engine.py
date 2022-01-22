from bs4 import BeautifulSoup
from time import sleep as actual_sleep
import requests
from random import randint
from html.parser import HTMLParser

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) '
    + 'Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:
    HTTP  = "http://"
    HTTPS = "https://"
    WWW   = "www."
    SLASH = "/"

    @staticmethod
    def search(query, sleep=True):
        #Prevents loading too many pages too soon
        if sleep: 
            actual_sleep(randint(20, 60)) #[10, 100] is conservative

        #Adds "+" between words for the query
        temp_url = '+'.join(query.split())
        url = 'http://www.ask.com/web?q=' + temp_url
        soup = BeautifulSoup(
            requests.get(url, headers=USER_AGENT).text,
            "html.parser")

        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all(
            'div',
            {'class': 'PartialSearchResults-item-title'})
        results = []
        processed_results = set() #Set to prevent duplicate results

        for result in raw_results:
            link = result.find('a').get('href')
            processed_link = SearchEngine.process_link(link)

            #URLs must not be duplicated
            if processed_link not in processed_results:
                processed_results.add(processed_link)
                results.append(link)

            #Only get 10 results
            if len(results) == 10:
                break

        return results

    @staticmethod
    def process_link(raw_link):
        link = raw_link

        if link.startswith(SearchEngine.HTTP):
            link = link[len(SearchEngine.HTTP):]

        if link.startswith(SearchEngine.HTTPS):
            link = link[len(SearchEngine.HTTPS):]

        if link.startswith(SearchEngine.WWW):
            link = link[len(SearchEngine.WWW):]

        if link.endswith(SearchEngine.SLASH):
            link = link[:-len(SearchEngine.SLASH)]

        return link

