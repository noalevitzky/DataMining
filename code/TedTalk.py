

class TedTalk:
    """representing a tedtalk and it's attributes"""

    def __init__(self, url, title, description, length, num_views, location, date, related_tags,
                 num_languages, num_comments, speaker_name, speaker_profession,
                 full_transcript, page_html):
        self.url = url
        self.title = title
        self.description = description
        self.length = length
        self.num_views = num_views
        self.location = location
        self.upload_date = date
        self.related_tags = related_tags
        self.num_languages = num_languages
        self.num_comments = num_comments
        self.speaker_name = speaker_name
        self.speaker_profession = speaker_profession
        self.full_transcript = full_transcript
        self.page_html = page_html

    def dict(self):
        return dict((k, v) for k, v in self.__dict__.items())
