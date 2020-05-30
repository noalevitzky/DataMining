from selenium import webdriver
from selenium import common
import time

PATH = "C:/Users/NO1/PycharmProjects/milestone1/chromedriver.exe"  # Driver is uploaded on GitHub
URL_for_transcript = "https://www.ted.com/talks/robert_waldinger_what_makes_a_good_life_lessons_from_the_longest_study_on_happiness/transcript"
URL = "https://www.ted.com/talks/malcolm_gladwell_the_unheard_story_of_david_and_goliath"
URL2 = "https://www.ted.com/talks/jon_ronson_strange_answers_to_the_psychopath_test?referrer=playlist-the_most_popular_talks_of_all"
driver = webdriver.Chrome(PATH)  # Make sure to have the latest chrome browser version, Adblock+, and chrome driver
driver.get(URL2)
time.sleep(6)  # Allows the page to load and update first, before the crawling begins


def url_transcript_gen(video_url):
    # Converts a regular TedTalk url into the transcript equivalent. Make sure the original url is without additions.
    return video_url + "/transcript"


def get_transcript():
    # Requires the driver to use the transcript video URL (helper function is provided)

    transcript_data = {}  # Formatted as {time: sentence}
    content = driver.find_element_by_css_selector(".m-b\:7")
    text_unparsed = content.find_elements_by_css_selector("div.Grid")
    for line in text_unparsed:
        row = line.text.strip().splitlines()
        try:
            timestamp = row[0]
            text = row[1]
            transcript_data[timestamp] = text
        except IndexError:
            print("Parsing error in transcript. Full row is:", row)
            print("url is:", URL)
    return transcript_data


def get_translations():
    # Requires the driver to use the transcript video URL

    content = driver.find_element_by_css_selector(".Form-input")
    languages = content.text.splitlines()
    return languages

def get_profession():
    # Requires the driver to use the main video URL
    content = driver.find_element_by_css_selector("span.d\:b:nth-child(2)")
    return content.text

def get_description():
    content = driver.find_element_by_css_selector(".w\:3of4\@md > p:nth-child(1)")
    return content.text

def get_length():
    content = driver.find_element_by_css_selector("span.f\:\.9:nth-child(1)")
    return content.text

def get_title():
    content = driver.find_element_by_css_selector("h1.f-w\:700:nth-child(3)")
    return content.text

def get_views():
    views = None
    try:
        content = driver.find_element_by_css_selector(".css-1uodv95")
        if content is not None:
            views = content.text.replace(",", "")
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", driver.current_url)
    finally:
        return views

def get_speaker():
    """returns the title of ted talk"""

    content = None
    try:
        content = driver.find_element_by_css_selector("span.l-h\:t")
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", driver.current_url)
    finally:
        return content.text if content is not None else content

def get_upload_date():
    """returns the upload date of ted talk"""

    content = None
    try:
        content = driver.find_element_by_css_selector("meta[itemprop='uploadDate']")
        print(content)
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", driver.current_url)
    finally:
        return content.get_attribute("content") if content is not None else content

def get_tags():
    # Requires the driver to use the transcript video URL

    tags = []
    try:
        content = driver.find_elements_by_css_selector("meta[property='og:video:tag']")
        if content:
            for line in content:
                tags.append(line.get_attribute("content"))
    except common.exceptions.NoSuchElementException:
        print("problem with translation css selector at", driver.current_url)
    finally:
        return tags

print(get_tags())

# Closes the last chrome window opened. Disable for debugging purposes
driver.close()
