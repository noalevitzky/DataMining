

class TedTalk:
    """representing a tedtalk and it's attributes"""

    def __init__(self, video_url, title, description, length, views,
                 upload_date, related_tags, translations, speaker_name,
                 speaker_profession, full_transcript, page_html):
        self.video_url = video_url
        self.title = title
        self.description = description
        self.length = length
        self.views = views
        self.upload_date = upload_date
        self.related_tags = related_tags
        self.translations = translations
        self.speaker_name = speaker_name
        self.speaker_profession = speaker_profession
        self.full_transcript = full_transcript
        self.page_html = page_html

    def dict(self):
        return dict((k, v) for k, v in self.__dict__.items())

