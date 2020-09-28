from collections import Counter
from datetime import date
import calendar

import csv

CSV_COLUMNS = ["layer", "reaction_counter", "avg_reaction_time", "avg_reaction_ratio", "avg_speaking_rate",
               "avg_sen_len", "avg_ques_num", "total_ques_asked", "total_ques_asked_by_type",
               "avg_ques_type", "avg_ratio_quality", "top_words"]


class AnalysisHandler:

    def __init__(self, top_list, mid_list, bot_list):
        self.top = top_list
        self.mid = mid_list
        self.bot = bot_list
        self.stack = []
        self.stack_mode = "all"

        self.avg_talk_len = None
        self.professions = []
        self.reaction_counter = []
        self.avg_reaction_time = None
        self.avg_reaction_ratio = None
        self.avg_speaking_rate = None
        self.avg_sen_len = None
        self.avg_ques_num = None
        self.total_ques_asked = None
        self.total_ques_asked_by_type = {}
        self.avg_ques_type = {}
        self.avg_ratio_quality = None
        self.top_words = []
        self.views_per_weekday = {}

    def filter_stack_by_tag(self, tag):
        """
        This function filters the stack by the tag, and updates it accordingly.
        :param tag: A string
        """
        filtered = []
        for talk in self.stack:
            if tag in talk.get_tags():
                filtered.append(talk)
        self.stack = filtered

    def load_stack(self, by_level="all"):
        """
        This function loads talks into the stack. Default is loading all of the talks.
        :param by_level: A string of "all" / "top" / "mid / "bot"
        """
        if by_level == "top":
            self.stack = self.top
            self.stack_mode = "top"
        elif by_level == "mid":
            self.stack = self.mid
            self.stack_mode = "mid"
        elif by_level == "bot":
            self.stack = self.bot
            self.stack_mode = "bot"
        elif by_level == "all":
            self.stack = self.top + self.mid + self.bot
            self.stack_mode = "all"
        else:
            self.stack = []
            self.stack_mode = ""

    def init_analysis(self):
        """
        Some of the analysis of each talk might take some time, especially when
        it's done in mass. This function will run these compute-heavy functions,
        and save the data in the objects. Then, it will pickle it, allowing the
        analysis to be done only once. Afterwards all the data is saved, and
        available for manipulation.
        """
        for talk in self.stack:
            # print(talk.get_title())
            talk.compute()
            # talk.print_engagement_stats()
            # talk.print_general_talk_stats()
            # print()

    # Calculations
    def count_professions(self):
        professions = []
        for talk in self.stack:
            professions.append(talk.get_profession())
        return Counter(professions)

    def get_views_per_weekday(self):
        # {"Weekday": ("total number of views", "total number of talks published that day")}
        views_per_weekday = {"Sunday": [0, 0], "Monday": [0, 0], "Tuesday": [0, 0], "Wednesday": [0, 0],
                             "Thursday": [0, 0], "Friday": [0, 0], "Saturday": [0, 0]}
        for talk in self.stack:
            date_st = talk.get_publication_date()
            date_p = date_st.split("T")[0].split("-")
            year, month, day = date_p
            date_dt = date(int(year), int(month), int(day))
            weekday = calendar.day_name[date_dt.weekday()]
            views_per_weekday[weekday][0] += talk.get_num_of_views()
            views_per_weekday[weekday][1] += 1
        return views_per_weekday

    def calc_avg_talk_length(self):
        lengths = []
        for talk in self.stack:
            num_of_minutes = round(float(talk.get_legnth()))
            lengths.append(num_of_minutes)
        avg = sum(lengths) / len(lengths)
        return round(avg, 1)

    def calc_reaction_counter(self):
        reaction_counter = {}
        for talk in self.stack:
            talk_reactions = talk.get_reaction_counter()
            for reaction, f in talk_reactions.items():
                reaction_counter[reaction] = reaction_counter.get(reaction, 0) + f
        return reaction_counter

    def calc_avg_reaction_time(self):
        times = []
        for talk in self.stack:
            times.append(talk.get_avg_reaction_time())
        avg = sum(times) / len(times)
        return round(avg)

    def calc_avg_reaction_ratio(self):
        reaction_ratio = []
        for talk in self.stack:
            reaction_ratio.append(talk.get_reaction_ratio())
        avg = sum(reaction_ratio) / len(reaction_ratio)
        return round(avg, 3)

    def calc_avg_speaking_rate(self):
        rate_lst = []
        for talk in self.stack:
            rate_lst.append(talk.get_speaking_rate())
        avg = sum(rate_lst) / len(rate_lst)
        return round(avg)

    def calc_avg_sentence_len(self):
        sen_len_lst = []
        for talk in self.stack:
            sen_len_lst.append(talk.get_avg_sentence_len())
        avg = sum(sen_len_lst) / len(sen_len_lst)
        return round(avg)

    def calc_avg_question_num(self):
        ques_num_lst = []
        for talk in self.stack:
            ques_num_lst.append(talk.get_num_of_questions())
        avg = sum(ques_num_lst) / len(ques_num_lst)
        return round(avg)

    def calc_total_questions_asked(self):
        ques_num_lst = []
        for talk in self.stack:
            ques_num_lst.append(talk.get_num_of_questions())
        return sum(ques_num_lst)

    def calc_total_questions_asked_by_type(self):
        t_ques_types = Counter()
        for talk in self.stack:
            t_ques_types += Counter(talk.get_question_types())
        return t_ques_types

    def calc_avg_question_types(self):
        t_ques_types = Counter()
        res = {}
        i = 0
        for talk in self.stack:
            t_ques_types += Counter(talk.get_question_types())
            i += 1
        for q, n in t_ques_types.most_common():
            res[q] = round(n / i)
        return res

    def calc_avg_ratio_quality_questions(self):
        avg_ratio = []
        for talk in self.stack:
            avg_ratio.append(talk.get_quality_question_ratio())
        avg = sum(avg_ratio) / len(avg_ratio)
        return round(avg, 2)

    def count_total_words(self):
        words_lst = []
        for talk in self.stack:
            words_lst += talk.get_words()
        return Counter(words_lst)

    def get_top_words(self, n):
        return self.count_total_words().most_common(n)

    # Stats Print-Functions
    def print_stats(self):
        self.reaction_counter = self.calc_reaction_counter()
        self.avg_reaction_time = self.calc_avg_reaction_time()
        self.avg_reaction_ratio = self.calc_avg_reaction_ratio()
        self.avg_speaking_rate = self.calc_avg_speaking_rate()
        self.avg_sen_len = self.calc_avg_sentence_len()
        self.professions = self.count_professions()
        self.avg_ques_num = self.calc_avg_question_num()
        self.total_ques_asked = self.calc_total_questions_asked()
        self.total_ques_asked_by_type = self.calc_total_questions_asked_by_type()
        self.avg_ques_type = self.calc_avg_question_types()
        self.avg_ratio_quality = self.calc_avg_ratio_quality_questions()
        self.top_words = self.get_top_words(30)
        self.avg_talk_len = self.calc_avg_talk_length()
        self.views_per_weekday = self.get_views_per_weekday()

        print("****** Analysis Result ******")
        print(f"Total profession count is: {self.professions}")
        print(f"Average Talk Length: {self.avg_talk_len} minutes")
        print(f"Reaction Counter: {self.reaction_counter}")
        print(f"Average Reaction Time: Once every {self.avg_reaction_time} seconds")
        print(f"Average Reaction Ratio: {self.avg_reaction_ratio}")
        print(f"Average Speaking Rate: {self.avg_speaking_rate} words per minute")
        print(f"Average Sentence Length: {self.avg_sen_len} words")
        print(f"Average Number Of Questions: {self.avg_ques_num}")
        print(f"Total Questions Asked: {self.total_ques_asked}")
        print(f"Total Questions Asked By Type: {self.total_ques_asked_by_type}")
        print(f"Average Types Of Questions: {self.avg_ques_type}")
        print(f"Average Question Quality ratio: {self.avg_ratio_quality}")
        print(f"Top 20 Words: {self.top_words}")
        print(f"Views Per Weekday Are: {self.views_per_weekday}")

    def save_to_csv(self, file_name):
        try:
            with open(file_name, 'a', newline='', encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
                writer.writeheader()
                writer.writerow({'layer': self.stack_mode,
                                 'reaction_counter': self.reaction_counter,
                                 'avg_reaction_time': self.avg_reaction_time,
                                 'avg_reaction_ratio': self.avg_reaction_ratio,
                                 'avg_speaking_rate': self.avg_speaking_rate,
                                 'avg_sen_len': self.avg_sen_len,
                                 'avg_ques_num': self.avg_ques_num,
                                 'total_ques_asked': self.total_ques_asked,
                                 'total_ques_asked_by_type': self.total_ques_asked_by_type,
                                 'avg_ques_type': self.avg_ques_type,
                                 'avg_ratio_quality': self.avg_ratio_quality,
                                 'top_words': self.top_words})
        except IOError:
            print("I/O error in creating CSV file")
            with open("output.txt", 'w', encoding="utf-8"):
                writer.writerow({'layer': self.stack_mode,
                                 'reaction_counter': self.reaction_counter,
                                 'avg_reaction_time': self.avg_reaction_time,
                                 'avg_reaction_ratio': self.avg_reaction_ratio,
                                 'avg_speaking_rate': self.avg_speaking_rate,
                                 'avg_sen_len': self.avg_sen_len,
                                 'avg_ques_num': self.avg_ques_num,
                                 'total_ques_asked': self.total_ques_asked,
                                 'total_ques_asked_by_type': self.total_ques_asked_by_type,
                                 'avg_ques_type': self.avg_ques_type,
                                 'avg_ratio_quality': self.avg_ratio_quality,
                                 'top_words': self.top_words})
