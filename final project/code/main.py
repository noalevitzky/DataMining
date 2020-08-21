import TedTalk as Tt
import AnalysisHandler as Ah
import preprocessor
from selenium import webdriver
from selenium import common
import time
import pickle
import os
import csv
import math

# global tedTalk object array
TED_TALKS = []

# tedTalks urls
POPULAR_URLS = 'output/popular_urls.txt'
UNPOPULAR_URLS = 'output/unpopular_urls.txt'
MIDDLE_URLS = 'output/middle_urls.txt'
TEST_URL = 'https://www.ted.com/talks/bill_gates_how_the_pandemic_will_shape_the_near_future'

# driver & csv format
DRIVER_PATH = "chromedriver.exe"
CSV_COLUMNS = ["video_url", "title", "description", "length",
               "length_in_minutes", "views", "upload_date", "related_tags",
               "translations", "speaker_name", "speaker_profession",
               "full_transcript"]
driver = webdriver.Chrome(DRIVER_PATH)

# pickle files
POPULAR_PICKLE = 'output/popular_talks.p'
MIDDLE_PICKLE = 'output/middle_talks.p'
UNPOPULAR_PICKLE = 'output/unpopular_talks.p'
TEST_PICKLE = 'output/check.p'

# Clean Pickle files ready for analysis
TOP_CP = 'output/cleaned_popular_talks.p'
MID_CP = 'output/cleaned_middle_talks.p'
BOT_CP = 'output/cleaned_unpopular_talks.p'

""" **************** cur settings ! **************** """
# peek cur pickle & url file
CUR_PICKLE = UNPOPULAR_PICKLE
CUR_URL = UNPOPULAR_URLS


# CSV files
# POPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/popular_talks2.csv'
# UNPOPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/unpopular_talks4.csv'
# MIDDLE_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/middle_talks3.csv'
# TEST_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/check.csv'

# def write_csv():
#     try:
#         with open(UNPOPULAR_CSV, 'w', newline='', encoding="utf-8") as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
#             writer.writeheader()
#             for data in TED_TALKS:
#                 writer.writerow(data)
#     except IOError:
#         print("I/O error in creating CSV file")
#         with open("output.txt", 'w', encoding="utf-8") as file:
#             for data in TED_TALKS:
#                 file.write(str(data))


def write_pickle():
    """ writes new one. uncomment if needed """
    # with open(CUR_PICKLE, 'wb') as fp:

    """ append to existing"""
    with open(CUR_PICKLE, 'ab') as fp:
        # This:
        for data in TED_TALKS:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)

        # Should be this:
        pickle.dump(TED_TALKS, fp, protocol=pickle.HIGHEST_PROTOCOL)


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
        length = get_length(driver)
        length_in_minutes = convert_len_to_minutes(length)

        # driver for regular page
        driver.get(url)
        profession = get_profession(driver)
        description = get_description(driver)
        views = get_views(driver)
        speaker_name = get_speaker(driver)
        title = get_title(driver)
        upload_date = get_upload_date(driver)
        tags = get_related_tags(driver)
    except Exception:
        raise Exception
    finally:
        print(url)

    # create TedTalk object and append to list
    obj = Tt.TedTalk(url, title, description, length, length_in_minutes, views,
                     upload_date, tags, translation, speaker_name, profession,
                     transcript)
    # TED_TALKS.append(obj.dict())
    TED_TALKS.append(obj)


def get_title(dr):
    """returns the title of ted talk"""

    content = None
    try:
        content = driver.find_element_by_css_selector(
            "h1.f-w\:700:nth-child(3)")
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", dr.current_url)
    finally:
        return content.text if content is not None else content


def get_views(dr):
    views = None
    try:
        content = driver.find_element_by_css_selector(".css-1uodv95")
        if content is not None:
            views = content.text.replace(",", "")
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", dr.current_url)
    finally:
        return views


def get_speaker(dr):
    """returns the speaker of ted talk"""

    content = None
    try:
        content = driver.find_element_by_css_selector("span.l-h\:t")
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", dr.current_url)
    finally:
        return content.text if content is not None else content


def get_upload_date(dr):
    """returns the upload date of ted talk"""

    content = None
    try:
        content = driver.find_element_by_css_selector(
            "meta[itemprop='uploadDate']")
    except common.exceptions.NoSuchElementException:
        print("problem with title css selector at", dr.current_url)
    finally:
        return content.get_attribute(
            "content") if content is not None else content


def get_related_tags(dr):
    # Requires the driver to use the transcript video URL

    tags = []
    try:
        content = driver.find_elements_by_css_selector(
            "meta[property='og:video:tag']")
        if content:
            for line in content:
                tags.append(line.get_attribute("content"))
    except common.exceptions.NoSuchElementException:
        print("problem with related tags css selector at", dr.current_url)
    finally:
        return tags


def get_description(dr):
    content = None
    try:
        content = dr.find_element_by_css_selector(
            ".w\:3of4\@md > p:nth-child(1)")
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
        if content:
            languages = content.text.splitlines()
    except common.exceptions.NoSuchElementException:
        print("problem with translation css selector at", dr.current_url)
    finally:
        return languages


def get_transcript(dr):
    # Requires the driver to use the transcript video URL
    # (helper function is provided)
    transcript_data = {}  # Formatted as {time: sentence}

    try:
        content = dr.find_element_by_css_selector(".m-b\:7")
        text_unparsed = content.find_elements_by_css_selector("div.Grid")
        for line in text_unparsed:
            row = line.text.strip().splitlines()
            try:
                timestamp = row[0]
                text = row[1]
                transcript_data[timestamp] = text
            except IndexError:
                print(
                    "Parsing error in transcript list (Separating timestamp and text). Full row is:",
                    row)
    except common.exceptions.NoSuchElementException:
        print("problem with transcript css selector at", dr.current_url)
    finally:
        return transcript_data


def get_length(dr):
    content = None
    try:
        content = driver.find_element_by_css_selector(
            "span.f\:\.9:nth-child(1)")
        if content is not None:
            content = content.text
            arr = content.split(':')

            # adjust format to hh:mm:ss
            # check if len < 1 hour
            if len(arr) == 2:
                # check if len < 10 minutes
                if len(arr[0]) == 1:
                    content = '0' + content
                content = '00:' + content
    except common.exceptions.NoSuchElementException:
        print("problem with length css selector at", dr.current_url)
    finally:
        return content


def convert_len_to_minutes(length):
    if length is None:
        return length

    arr = length.split(':')
    return str((int(arr[0]) * 60) + int(arr[1]) + (int(arr[2]) / 60))


def url_transcript_gen(video_url):
    # Converts a regular TedTalk url into the transcript equivalent.
    # Make sure the original url is without additions.
    return video_url + "/transcript"


if __name__ == "__main__":
    # start_time = time.time()
    # try:
    #     with open(CUR_URL) as f:
    #         talks_urls = f.read().splitlines()
    #
    #         # //
    #         # batch = 30
    #         # total_parts = math.ceil(len(talks_urls) / batch)
    #         #
    #         # for i in range(3, total_parts):
    #         #     start = i * batch
    #         #     end = start + batch
    #         #     if end >= len(talks_urls):
    #         #         end = -1
    #         # //
    #
    #         for i, talk_url in enumerate(talks_urls[800:]):
    #             print("--- %s seconds ---" % (time.time() - start_time))
    #             print(str(i), " ", talk_url)
    #             create_talk(talk_url)
    #
    # finally:
    #     # write_csv()
    #     write_pickle()
    #     # time.sleep(15)
    driver.quit()

    pickle_in_1 = open(TOP_CP, "rb")
    pickle_in_2 = open(MID_CP, "rb")
    pickle_in_3 = open(BOT_CP, "rb")
    top_list = preprocessor.process_pickle(TOP_CP)[:183]
    mid_list = preprocessor.process_pickle(MID_CP)[:183]
    bot_list = preprocessor.process_pickle(BOT_CP)

    print(len(top_list), len(mid_list), len(bot_list))
    talk_ah = Ah.AnalysisHandler(top_list, mid_list, bot_list)
    print("***** ALL ANALYSIS *****")
    talk_ah.load_stack("all")
    talk_ah.init_analysis()
    talk_ah.print_stats()
    talk_ah.save_to_csv("layers_analyzed.csv")
    print("***** TOP ANALYSIS *****")
    talk_ah.load_stack("top")
    talk_ah.init_analysis()
    talk_ah.print_stats()
    talk_ah.save_to_csv("layers_analyzed.csv")
    print("***** MID ANALYSIS *****")
    talk_ah.load_stack("mid")
    talk_ah.init_analysis()
    talk_ah.print_stats()
    talk_ah.save_to_csv("layers_analyzed.csv")
    print("***** BOT ANALYSIS *****")
    talk_ah.load_stack("bot")
    talk_ah.init_analysis()
    talk_ah.print_stats()
    talk_ah.save_to_csv("layers_analyzed.csv")


# --- test ---
# create_talk(TEST_URL)
# write_pickle()
# driver.quit()
