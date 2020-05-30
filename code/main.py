import TedTalk as Tt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import common
import time
import csv
import math
# global tedTalk object array
TED_TALKS = []
TED_PAGES_TXT_PATH = "C:/Users/NO1/PycharmProjects/milestone1/ted_pages.txt"
DRIVER_PATH = "C:/Users/NO1/PycharmProjects/milestone1/chromedriver.exe"
CSV_COLUMNS = ["video_url", "title", "description", "length", "views",
               "upload_date", "related_tags", "translations", "speaker_name",
               "speaker_profession", "full_transcript", "page_html"]
driver = webdriver.Chrome(DRIVER_PATH)


def write_csv(file_name):
    csv_file = file_name + "_Top_Viewed.csv"
    try:
        with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for data in TED_TALKS:
                writer.writerow(data)
    except IOError:
        print("I/O error in creating CSV file")
        with open("output.txt", 'w', encoding="utf-8") as file:
            for data in TED_TALKS:
                file.write(str(data))


def create_talk(url):
    # init driver
    # Make sure to have the latest chrome browser version,
    # Adblock+, and chrome driver

    try:
        # driver for /transcript page
        # Allows the page to load and update first, before the crawling begins
        driver.get(url_transcript_gen(url))
        time.sleep(8)
        translation = get_translations(driver)
        transcript = get_transcript(driver)
        # driver for regular page
        driver.get(url)
        profession = get_profession(driver)
        description = get_description(driver)
    # except Exception:
    #     raise Exception
    finally:
        # Closes the last chrome window opened. Disable for debugging purposes
        # driver.close()
        print(url)
    time.sleep(5)
    # init beautiful soup
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')

    try:
        title = get_title(bs)
        length = get_length(bs)
        views = get_views(bs)
        upload_date = get_upload_date(bs)
        tags = get_related_tags(bs)
        speaker_name = get_speaker(bs)
    except Exception:
        raise Exception
    # html_str = str(bs.prettify())
    html_str = None
    # create TedTalk object and append to list
    obj = Tt.TedTalk(url, title, description, length, views, upload_date,
                     tags, translation, speaker_name, profession, transcript, html_str)
    TED_TALKS.append(obj.dict())


def get_title(bs):
    """returns the title of ted talk"""
    if len(list(bs.head.stripped_strings)) == 0:
        return None
    else:
        s = list(bs.head.stripped_strings)[0]
        if ": " in s:
            s = s.split(": ")[1]
        if " |" in s:
            s = s.split(" |")[0]
        return s


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

def get_description(dr):
    content = None
    try:
        content = dr.find_element_by_css_selector(".w\:3of4\@md > p:nth-child(1)")
    except common.exceptions.NoSuchElementException:
        print("problem with description css selector at", dr.current_url)
    finally:
        return content.text if content is not None else content

def get_profession(dr):
    # Requires the driver to use the main video URL
    content = None
    try:
        content = dr.find_element_by_css_selector("span.d\:b:nth-child(2)")
    except common.exceptions.NoSuchElementException:
        print("problem with profession css selector at", dr.current_url)
    finally:
        return content.text if content is not None else content


def get_translations(dr):
    # Requires the driver to use the transcript video URL

    languages = None
    try:
        content = driver.find_element_by_css_selector(".Form-input")
        languages = content.text.splitlines()
    except common.exceptions.NoSuchElementException:
        print("problem with translation css selector at", dr.current_url)
    finally:
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
    return transcript_data


def url_transcript_gen(video_url):
    # Converts a regular TedTalk url into the transcript equivalent.
    # Make sure the original url is without additions.
    return video_url + "/transcript"


if __name__ == "__main__":
    with open(TED_PAGES_TXT_PATH) as f:
        talks_urls = f.read().splitlines()
        batch = 30
        total_parts = math.ceil(len(talks_urls)/batch)

        for i in range(total_parts):
            start = i * batch
            end = start + batch
            if end >= len(talks_urls):
                end = -1
            for talk_url in talks_urls[start:end]:
                create_talk(talk_url)
            write_csv(str(start) + "-" + str(end))
            time.sleep(15)

        driver.quit()
