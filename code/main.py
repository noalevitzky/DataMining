import TedTalk as Tt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# global tedTalk object array
TED_TALKS = []
TED_PAGES_TXT = "C:/Users/Noa/Desktop/huji/second year/dataMining/milestone1/code/ted_pages.txt"
PATH = "C:/Users/Noa/Desktop/huji/second year/dataMining/milestone1/code/chromedriver.exe"  # Driver is uploaded on GitHub


# URL_for_transcript = "https://www.ted.com/talks/sir_ken_robinson_do_schools_kill_creativity/transcript?referrer=playlist-the_most_popular_talks_of_all"
# URL = "https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are?referrer=playlist-the_most_popular_talks_of_all&language=en"


def create_talk(talk_url):
    # init beautiful soup
    page = requests.get(talk_url)
    bs = BeautifulSoup(page.text, 'html.parser')

    # init driver
    driver = webdriver.Chrome(
        PATH)  # Make sure to have the latest chrome browser version, Adblock+, and chrome driver

    # driver for /transcript page
    driver.get(url_transcript_gen(talk_url))
    # Allows the page to load and update first, before the crawling begins
    time.sleep(6)
    translation = get_translations(driver)
    transcript = get_transcript(driver)

    # driver for regular page
    driver.get(talk_url)
    profession = get_profession(driver)

    # Closes the last chrome window opened. Disable for debugging purposes
    driver.close()

    obj = Tt.TedTalk(
        talk_url,
        get_title(bs),
        get_description(bs),
        get_length(bs),
        get_views(bs),
        get_upload_date(bs),
        get_related_tags(bs),
        translation,
        get_speaker(bs),
        profession,
        transcript,
        bs.prettify()
    )

    TED_TALKS.append(obj.dict())


def get_title(bs):
    """returns the title of ted talk"""
    s = bs.head.stripped_strings
    return list(s)[0].split(": ")[1].split(" |")[0]


def get_description(bs):
    ds = bs.find_all("meta", property="og:description")
    return ds[0].get("content")


def get_length(bs):
    s = bs.find(class_="main talks-main").stripped_strings
    return list(s)[3].replace("• ", "")


def get_views(bs):
    s = bs.find(class_="main talks-main").stripped_strings
    return list(s)[1].replace(",", "")


def get_speaker(bs):
    t = bs.find_all("title")
    return t[0].text.split(":")[0]


def get_upload_date(bs):
    """get upload date"""
    date = bs.find_all("meta", itemprop="uploadDate")
    return date[0].get("content")


def get_related_tags(bs):
    tags = bs.find_all("meta", property="og:video:tag")
    return [tag.get("content") for tag in tags]


def get_profession(dr):
    # Requires the driver to use the main video URL
    content = dr.find_element_by_css_selector("span.d\:b:nth-child(2)")
    return content.text


def get_translations(dr):
    # Requires the driver to use the transcript video URL
    content = dr.find_element_by_css_selector(".Form-input")
    languages = content.text.splitlines()
    return languages


def get_transcript(dr):
    # Requires the driver to use the transcript video URL
    # (helper function is provided)
    transcript_data = {}  # Formatted as {time: sentence}
    content = dr.find_element_by_css_selector(".m-b\:7")
    text_unparsed = content.find_elements_by_css_selector("div.Grid")
    for line in text_unparsed:
        row = line.text.strip().splitlines()
        try:
            timestamp = row[0]
            text = row[1]
            transcript_data[timestamp] = text
        except IndexError:
            print("Parsing error in transcript. Full row is:", row)
            # print("url is:", talk_url)
    return transcript_data


def url_transcript_gen(video_url):
    # Converts a regular TedTalk url into the transcript equivalent.
    # Make sure the original url is without additions.
    return video_url + "/transcript"


if __name__ == "__main__":
    with open(TED_PAGES_TXT) as f:
        talks_urls = f.read().splitlines()
        for talk_url in talks_urls[:1]:
            create_talk(talk_url)

        
        # todo: export TED_TALKS to csv file
