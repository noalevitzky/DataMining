import TedTalk as Tt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# global tedTalk object array
TED_TALKS = []
TED_PAGES_TXT_PATH = "C:/Users/Noa/Desktop/huji/second year/dataMining/milestone1/code/ted_pages.txt"
DRIVER_PATH = "C:/Users/Noa/Desktop/huji/second year/dataMining/milestone1/code/chromedriver.exe"
CSV_COLUMNS = ["video_url", "title", "description", "length", "views",
               "upload_date", "related_tags", "translations", "speaker_name",
               "speaker_profession", "full_transcript", "page_html"]


def write_csv():
    csv_file = "most_viewed_talks.csv"
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
    driver = webdriver.Chrome(DRIVER_PATH)

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
    # except Exception:
    #     raise Exception
    finally:
        # Closes the last chrome window opened. Disable for debugging purposes
        driver.close()

    # init beautiful soup
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')

    try:
        title = get_title(bs)
        description = get_description(bs)
        length = get_length(bs)
        views = get_views(bs)
        upload_date = get_upload_date(bs)
        tags = get_related_tags(bs)
        speaker_name = get_speaker(bs)
    except Exception:
        raise Exception

    # crete TedTalk object and append to list
    obj = Tt.TedTalk(url, title, description, length, views, upload_date,
                     tags, translation, speaker_name, profession, transcript,
                     str(bs.prettify()))
    TED_TALKS.append(obj.dict())


def get_title(bs):
    """returns the title of ted talk"""
    s = list(bs.head.stripped_strings)[0]
    if ": " in s:
        s = s.split(": ")[1]
    if " |" in s:
        s = s.split(" |")[0]
    return s


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
    with open(TED_PAGES_TXT_PATH) as f:
        talks_urls = f.read().splitlines()
        for talk_url in talks_urls[:3]:
            time.sleep(3)
            create_talk(talk_url)

        write_csv()
