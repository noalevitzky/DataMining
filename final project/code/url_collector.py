import requests
from bs4 import BeautifulSoup
import time

LINKS_PATH = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/links.txt'
POPULAR_URLS = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/popular_urls.txt'
UNPOPULAR_URLS = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/unpopular_urls2.txt'
MIDDLE_URLS = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/middle_urls.txt'

cache = []

""" **************** cur settings ! **************** """


# peek cur url & dest file

def write_links():
    """writes caches TedTalk pages to file"""
    # try:
    with open(UNPOPULAR_URLS, 'w') as file:
        for item in cache:
            file.write("%s\n" % item)

    # except:
    #     print('ERROR in creating file')


def get_link_tedpages(link):
    """
    :param link: link of top-viewed TedTalks
    :return: caches all TedTalk in link
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    items = soup.find(class_="talks-body").find(id="shoji") \
        .find(class_="shoji__door").find(class_="page shoji__washi") \
        .find(class_="main talks-main").find(id="browse-results") \
        .find(class_="row row-sm-4up row-lg-6up row-skinny") \
        .find_all(class_="col")
    for i, item in enumerate(items):
        current = "https://www.ted.com"
        cache.append(
            current + item.find(class_="media__message").a.get('href'))


if __name__ == "__main__":
    """ generates ted_pages.txt """

    with open(LINKS_PATH) as f:
        links = f.read().splitlines()
        start_time = time.time()

        for link in links[64:77]:
            time.sleep(2)
            # Troubleshooting:
            print("--- %s seconds ---" % (time.time() - start_time))
            print(link)
            get_link_tedpages(link)

        write_links()
