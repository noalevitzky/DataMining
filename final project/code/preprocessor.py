import pandas as pd
import pickle
import csv

POPULAR_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/popular_talks.p'
MIDDLE_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/middle_talks.p'
UNPOPULAR_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/unpopular_talks.p'
TEST_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/check.p'

CLEANED_POPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_popular.csv'
CLEANED_MIDDLE_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_middle.csv'
CLEANED_UNPOPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_unpopular.csv'

COLUMNS = ['video_url', 'title', 'description', 'length', 'length_in_minutes',
           'views', 'upload_date', 'related_tags', 'translations',
           'speaker_name', 'speaker_profession']

POPULAR, MIDDLE, UNPOPULAR = None, None, None


# ******** CSV ********

# popular_path = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/popular_talks_all.csv'
# middle_path = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/middle_talks_all.csv'
# unpopular_path = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/unpopular_talks_all.csv'

# POPULAR = pd.read_csv(popular_path, usecols=CSV_COLUMNS)
# MIDDLE = pd.read_csv(middle_path, usecols=CSV_COLUMNS)
# UNPOPULAR = pd.read_csv(unpopular_path, usecols=CSV_COLUMNS)

# DF_POPULAR = pd.DataFrame(POPULAR)
# DF_MIDDLE = pd.DataFrame(MIDDLE)
# DF_UNPOPULAR = pd.DataFrame(UNPOPULAR)
# DF_TEST = pd.DataFrame(TEST)

# CSV_COLUMNS = ["video_url", "title", "description", "length",
#                "length_in_minutes", "views", "upload_date", "related_tags",
#                "translations", "speaker_name", "speaker_profession",
#                "full_transcript"]

# def CSV_print_na_values(s):
#     print(s + ' removal - rows with missing vals:\n')
#     popular_data = DF_POPULAR.loc[DF_POPULAR.isna().values.any(axis=1)]
#     middle_data = DF_MIDDLE.loc[DF_MIDDLE.isna().values.any(axis=1)]
#     unpopular_data = DF_UNPOPULAR.loc[DF_UNPOPULAR.isna().values.any(axis=1)]
#
#     print('popular:\n', popular_data, '\n****\nmiddle:\n', middle_data,
#           '\n****\nunpopular:\n', unpopular_data)
#
#
# def CSV_remove_rows_with_missing_values():
#     """remove empty cells"""
#     DF_POPULAR.dropna(how='any', subset=['length', 'views', 'upload_date'],
#                       axis=0, inplace=True)
#     DF_MIDDLE.dropna(how='any', subset=['length', 'views', 'upload_date'],
#                      axis=0, inplace=True)
#     DF_UNPOPULAR.dropna(how='any', subset=['length', 'views', 'upload_date'],
#                         axis=0, inplace=True)
#
#
# def CSV_find_overflows():
#     print('overflows:\n')
#     popular_data = DF_POPULAR[
#         DF_POPULAR['video_url'].str.contains('http', na=False) == False]
#     middle_data = DF_MIDDLE[
#         DF_MIDDLE['video_url'].str.contains('http', na=False) == False]
#     unpopular_data = DF_UNPOPULAR[
#         DF_UNPOPULAR['video_url'].str.contains('http', na=False) == False]
#
#     print('popular:\n', popular_data, '\n****\nmiddle:\n', middle_data,
#           '\n****\nunpopular:\n', unpopular_data)
#
#
# def CSV_validate_no_rows_without_transcript():
#     print('num of rows without transcript:')
#     print('POPULAR:',
#           DF_POPULAR.loc[DF_POPULAR['full_transcript'] == '{}'].size)
#     print('MIDDLE:',
#           DF_MIDDLE.loc[DF_MIDDLE['full_transcript'] == '{}'].size)
#     print('UNPOPULAR:',
#           DF_UNPOPULAR.loc[DF_UNPOPULAR['full_transcript'] == '{}'].size)
#

# ******** END CSV ********

def write_csv_without_transcript(dest, source):
    try:
        with open(dest, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            writer.writeheader()
            for data in source:
                writer.writerow(data.dict_without_transcript())
    except IOError:
        print("I/O error in creating CSV file")
        with open("output.txt", 'w', encoding="utf-8") as file:
            for data in source:
                file.write(str(data))


def remove_talks_with_missing_values(lst):
    """ remove empty cells """
    return [talk for talk in lst if
            talk.length and talk.views and talk.upload_date]


def remove_talks_without_transcript(lst):
    """ remove empty cells """
    return [talk for talk in lst if len(talk.full_transcript.keys()) > 1]


def create_df(lst):
    """ creates df without transcript """
    return pd.DataFrame(
        [[getattr(i, j) for j in COLUMNS] for i in lst],
        columns=COLUMNS)


def process_pickle(url):
    """ load all obj in pickle to list """
    data = []
    with open(url, 'rb') as f:
        while True:
            try:
                o = pickle.load(f)
            except EOFError:
                break
            data.append(o)
    return data


if __name__ == '__main__':
    # //
    # prev - CSV
    # CSV_find_overflows()
    # # todo remove bill's interview
    # CSV_print_na_values('BEFORE')
    # CSV_remove_rows_with_missing_values()
    # CSV_print_na_values('AFTER')
    # CSV_validate_no_rows_without_transcript()
    # //

    """ data cleaning """
    # POPULAR
    print('POPULAR')
    POPULAR = process_pickle(POPULAR_PICKLE)
    print('original: ', len(POPULAR))
    POPULAR = remove_talks_without_transcript(POPULAR)
    print('transcript:', len(POPULAR))
    POPULAR = remove_talks_with_missing_values(POPULAR)
    print('values:', len(POPULAR))

    # MIDDLE
    print('\nMIDDLE')
    MIDDLE = process_pickle(MIDDLE_PICKLE)
    print('original: ', len(MIDDLE))
    MIDDLE = remove_talks_without_transcript(MIDDLE)
    print('transcript:', len(MIDDLE))
    MIDDLE = remove_talks_with_missing_values(MIDDLE)
    print('values:', len(MIDDLE))

    # UNPOPULAR
    print('\nUNPOPUAR')
    UNPOPULAR = process_pickle(UNPOPULAR_PICKLE)
    print('original: ', len(UNPOPULAR))
    UNPOPULAR = remove_talks_without_transcript(UNPOPULAR)
    print('transcript:', len(UNPOPULAR))
    UNPOPULAR = remove_talks_with_missing_values(UNPOPULAR)
    print('values:', len(UNPOPULAR))

    """ reality check """

    # export to CSV without transcript, after cleaning
    write_csv_without_transcript(CLEANED_POPULAR_CSV, POPULAR)
    write_csv_without_transcript(CLEANED_MIDDLE_CSV, MIDDLE)
    write_csv_without_transcript(CLEANED_UNPOPULAR_CSV, UNPOPULAR)

    # check for duplicates in crawling

    # df_popular = create_df(POPULAR)
    # df_middle = create_df(MIDDLE)
    # df_unpopular = create_df(UNPOPULAR)

    # df_popular_nodup = df_popular.drop_duplicates()
    # df_middle_nodup = df_middle.drop_duplicates()
    # df_unpopular_nodup = df_unpopular.drop_duplicates()

    # print('popular:', df_popular.count(), df_popular_nodup.count())
    # print('middle:', df_middle.count(), df_middle_nodup.count())
    # print('unpopular:', df_unpopular.count(), df_unpopular_nodup.count())
