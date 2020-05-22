import requests
from bs4 import BeautifulSoup
import time

cache = []


def write_links():
    """
    writes caches TedTalk pages to file
    """
    try:
        with open('code/ted_pages.txt', 'w') as file:
            for item in cache:
                file.write("%s\n" % item)
    except:
        print('ERROR in creating json')
    finally:
        file.close()


def get_link_tedpages(link):
    """
    :param link: link of top-viewed TedTalks
    :return: caches all TedTalk in link
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    items = soup.find(class_="talks-body").find(id="shoji")\
        .find(class_="shoji__door").find(class_="page shoji__washi")\
        .find(class_="main talks-main").find(id="browse-results")\
        .find(class_="row row-sm-4up row-lg-6up row-skinny")\
        .find_all(class_="col")
    for i, item in enumerate(items):
        current = "https://www.ted.com"
        cache.append(current+item.find(class_="media__message").a.get('href'))


if __name__ == "__main__":
    """ generates ted_pages.txt """

    with open("code/links.txt") as f:
        links = f.read().splitlines()
        start_time = time.time()

        for link in links[:13]:
            time.sleep(2)
            # Troubleshooting:
            # print("--- %s seconds ---" % (time.time() - start_time))
            # print(link)
            get_link_tedpages(link)

        write_links()
