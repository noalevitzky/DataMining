from selenium import webdriver
import time

PATH = "C:/Users/NO1/PycharmProjects/milestone1/chromedriver.exe"  # Driver is uploaded on GitHub
URL_for_transcript = "https://www.ted.com/talks/robert_waldinger_what_makes_a_good_life_lessons_from_the_longest_study_on_happiness/transcript"
URL = "https://www.ted.com/talks/malcolm_gladwell_choice_happiness_and_spaghetti_sauce"
driver = webdriver.Chrome(PATH)  # Make sure to have the latest chrome browser version, Adblock+, and chrome driver
driver.get(URL)
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

print(get_length())

# Closes the last chrome window opened. Disable for debugging purposes
driver.close()