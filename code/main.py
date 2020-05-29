import TedTalk as Tt
import requests
from bs4 import BeautifulSoup

# global tedTalk object array
TED_TALKS = []


def create_talk(talk_url):
    page = requests.get(talk_url)
    bs = BeautifulSoup(page.text, 'html.parser')

    # todo: full_transcript
    # todo: speaker_profession
    # todo optional: num_languages (under Transcript page)
    # todo optional: num_comments
    # todo optional: location (TEDSummit, TED2019 (above related tags section)
    obj = Tt.TedTalk(
        talk_url,
        get_title(bs),
        get_length(bs),
        get_description(bs),
        get_views(bs),
        location,
        get_upload_date(bs),
        get_related_tags(bs),
        num_languages,
        num_comments,
        get_speaker(bs),
        speaker_profession,
        full_transcript,
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


if __name__ == "__main__":
    with open("code/ted_pages.txt") as f:
        talks_urls = f.readlines()
        for talk_url in talks_urls:
            create_talk(talk_url)

        # todo: export TED_TALKS to csv file