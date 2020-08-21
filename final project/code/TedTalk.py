import re
from collections import Counter
from datetime import datetime
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from stop_words import get_stop_words
# import nltk
# nltk.download('wordnet')
# nltk.download('punkt')
LEMMATIZER = WordNetLemmatizer()
QUESTION_WORD_LST = ["who", "why", "what", "where", "when", "how"]
STOP_SIGNS = [',', '.', "'", '"', '`', ';', "''", '""', "``", ']', '[', '(',
              ')', ':', "?", "!", "...", "--", '’']


class TedTalk:
    """representing a tedtalk and it's attributes"""

    def __init__(self, video_url, title, description, length,
                 length_in_minutes, views, upload_date, related_tags,
                 translations, speaker_name , speaker_profession,
                 full_transcript):
        self.video_url = video_url
        self.title = title
        self.description = description
        self.length = length
        self.length_in_minutes = length_in_minutes
        self.views = views
        self.upload_date = upload_date
        self.related_tags = related_tags
        self.translations = translations
        self.speaker_name = speaker_name
        self.speaker_profession = speaker_profession
        self.full_transcript = full_transcript

        # Computed Variables
        self.transcript_parsed_str = ""
        self.tokenized_sentences = []
        self.tokenized_words = []
        self.lemmatized_words = []

        # Analysed Data
        self.reaction_timeline = []
        self.reaction_counter = []
        self.avg_reaction_time = []
        self.reaction_ratio = []
        self.speaking_rate = []
        self.avg_sen_len = []
        self.num_of_questions = []
        self.question_types = []
        self.quality_question_ratio = []

    def dict(self):
        return dict((k, v) for k, v in self.__dict__.items())

    def dict_without_transcript(self):
        return dict((k, v) for k, v in self.__dict__.items() if k != 'full_transcript')

    # GETTERS
    def get_words(self):
        return self.lemmatized_words

    def get_tags(self):
        return self.related_tags

    def get_reaction_counter(self):
        return self.reaction_counter

    def get_avg_reaction_time(self):
        return self.avg_reaction_time

    def get_reaction_ratio(self):
        return self.reaction_ratio

    def get_speaking_rate(self):
        return self.speaking_rate

    def get_title(self):
        return self.title

    def get_num_of_sentences(self):
        return len(self.tokenized_sentences)

    def get_avg_sentence_len(self):
        return self.avg_sen_len

    def get_num_of_questions(self):
        return self.num_of_questions

    def get_question_types(self):
        return self.question_types

    def get_quality_question_ratio(self):
        return self.quality_question_ratio

    # Main handlers for this class
    def analyze(self):
        """
        Called by compute(). This Function sets all variables under the
        "Analysed Data" section in the constructor.
        """
        self.reaction_timeline = self.create_reaction_timeline()
        self.reaction_counter = self.calc_reaction_counter(self.reaction_timeline)
        self.avg_reaction_time = self.calc_avg_reaction_time(self.reaction_timeline)
        self.reaction_ratio = self.calc_reaction_ratio(self.reaction_counter)
        self.speaking_rate = self.calc_speaking_rate()
        self.avg_sen_len = self.calc_avg_sentence_len()
        self.num_of_questions = len(self.count_all_questions())
        self.question_types = self.count_types_of_questions(self.count_all_questions())
        self.quality_question_ratio = self.calc_questions_quality_ratio(self.count_all_questions(), self.question_types)

    def compute(self):
        """
        This function manages all the heavy-lifting functions,
        and then analyzes the results. After compute() is called,
        it's recommended to pickle the files for faster use in the future.
        """
        self.transcript_parsed_str = self.parse_transcript_to_str()
        self.tokenized_sentences = self.tokenize_transcript_to_sentences()
        raw_nltk_words = self.tokenize_transcript_to_words()
        self.tokenized_words = self.filter_chars_from_word_lst(raw_nltk_words)
        self.lemmatized_words = self.lemmatize_words()

        # Using the raw data to calculate the data
        self.analyze()

    # NLTK & POS Tagging Functions
    def tokenize_transcript_to_sentences(self):
        tokenized = sent_tokenize(self.transcript_parsed_str)
        return tokenized

    def tokenize_transcript_to_words(self):
        tokenized = word_tokenize(self.transcript_parsed_str)
        return tokenized

    def lemmatize_words(self):
        """
        This Function Removes stop words, and lemmatizes the tokenized words according to their meaning.
        :return: A list of lemmatized words
        """
        tokens = self.tokenized_words
        filter_lst = get_stop_words('english') + ["'s", "n't", "'re", "u", "'m", "'ve", "can", "one", "like", "just", "thing", "s"]
        lemmatized = []

        # Removing stop words
        tokens_no_sw = [w for w in tokens if w.lower() not in filter_lst]

        # Lemmatizing
        for pair in tokens_no_sw:
            lemmatized.append(LEMMATIZER.lemmatize(pair).lower())
        return lemmatized

    # General NLP Helper Functions
    def parse_transcript_to_str(self):
        talk = ""
        for p in self.full_transcript.values():
            if "(" not in p:
                talk += " "
                talk += p.lower()
        return talk

    def filter_chars_from_word_lst(self, word_list):
        filtered = [w for w in word_list if w not in STOP_SIGNS]
        return filtered

    def count_all_questions(self):

        questions_list = []
        for sentence in self.tokenized_sentences:
            if "?" in sentence:
                questions_list.append(sentence)
        return questions_list

    def count_types_of_questions(self, questions_list):
        questions_types = {}
        for wrd in QUESTION_WORD_LST:
            for question in questions_list:
                if wrd in question:
                    questions_types[wrd] = questions_types.get(wrd, 0) + 1
        return questions_types

    # TODO: FIX THE TIME FORMAT TO XX:XX:XX. THIS IS HARDCODED!
    def create_reaction_timeline(self):
        """
        :return: A dictionary of {timestamp (str): reaction (str}
        """

        timeline = [('00:00', ['START'])]

        for time, para in self.full_transcript.items():

            # Extracting all text between the parenthesis
            reaction = re.findall(r'\((.*?) *\)', para)
            if reaction and ("In" not in reaction[0]):

                timeline.append((time, reaction))

        len_parsed = self.length
        len_unparsed = self.length.split(":")
        if len(len_unparsed) == 3:
            h = len_unparsed[0]
            m = len_unparsed[1]
            s = len_unparsed[2]
            min = int(h) * 60 + int(m)
            len_parsed = str(min) + ":" + s
        timeline.append((len_parsed, ['END']))
        return timeline

    def calc_reaction_counter(self, timeline):

        reaction_lst = []
        for moment in timeline:
            time, reactions = moment
            if ('START' not in reactions) and ('END' not in reactions):
                for reaction in reactions:
                    reaction_lst.append(reaction)
        return Counter(reaction_lst)

    def calc_avg_reaction_time(self, reaction_timeline):

        timestamp_list = []
        for reactions in reaction_timeline:
            time, response = reactions
            d_time = datetime.strptime(time, '%M:%S')
            timestamp_list.append(d_time)

        # The difference between every consecutive pair
        duration = [timestamp_list[i + 1] - timestamp_list[i] for i in range(len(timestamp_list) - 1)]

        # Average calculation
        duration_sum = 0
        for time in duration:
            duration_sum += time.total_seconds()

        avg_response_time = round(duration_sum / len(duration))

        return avg_response_time

    def calc_reaction_ratio(self, reaction_counter):
        """
        Responsive rate = number of reactions / total num of sentences
        :param reaction_counter:
        :return:
        """
        rate = sum(reaction_counter.values()) / self.get_num_of_sentences()
        return round(rate, 3)

    def calc_speaking_rate(self):
        num_of_minutes = round(float(self.length_in_minutes))
        rate = len(self.tokenized_words) / num_of_minutes
        return round(rate)

    def calc_avg_sentence_len(self):
        sentence_avg_len = round(len(self.tokenized_words) / len(self.tokenized_sentences))
        return sentence_avg_len

    def calc_questions_quality_ratio(self, question_list, question_types):
        if not question_list:
            return 0
        else:
            return round(sum(question_types.values()) / len(question_list), 2)

    # Stats Print-Functions
    def print_engagement_stats(self):
        print("****** Audience Engagement Stats ******")
        print(f"Reaction Timeline: {self.reaction_timeline}")
        print(f"Reaction Counter: {self.reaction_counter}")
        print(f"Average Reaction time: Once every {self.avg_reaction_time} seconds")
        print(f"Reaction Ratio: {self.reaction_ratio}")

    def print_general_talk_stats(self):
        print("****** General Talk Stats ******")
        print(f"Average Speaking Rate: {self.speaking_rate} words per minute")
        print(f"Average Sentence Length: {self.avg_sen_len} words")
        print(f"Number Of Questions Asked: {self.num_of_questions}")
        print(f"Types Of Questions: {self.question_types}")
        print(f"Questions Quality Ratio: {self.quality_question_ratio}")
