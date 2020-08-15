import pandas as pd
import pickle
import csv

# original pickles from crawling
POPULAR_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/popular_talks.p'
MIDDLE_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/middle_talks.p'
UNPOPULAR_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/unpopular_talks.p'
TEST_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/check.p'

# cleaned pickle
CLEANED_POPULAR_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_popular_talks.p'
CLEANED_MIDDLE_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_middle_talks.p'
CLEANED_UNPOPULAR_PICKLE = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_unpopular_talks.p'

# cleaned csv
CLEANED_POPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_popular.csv'
CLEANED_MIDDLE_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_middle.csv'
CLEANED_UNPOPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/cleaned_unpopular.csv'

COLUMNS_NO_TRANSCRIPT = ['video_url', 'title', 'description', 'length',
                         'length_in_minutes', 'views', 'upload_date',
                         'related_tags', 'translations', 'speaker_name',
                         'speaker_profession']


def write_csv_without_transcript(dest, source):
    try:
        with open(dest, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS_NO_TRANSCRIPT)
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
        [[getattr(i, j) for j in COLUMNS_NO_TRANSCRIPT] for i in lst],
        columns=COLUMNS_NO_TRANSCRIPT)


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


def write_pickle(p_file, lst):
    with open(p_file, 'wb') as fp:
        for data in lst:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
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

    # export to CSV without transcript
    # export to pickle
    write_csv_without_transcript(CLEANED_POPULAR_CSV, POPULAR)
    write_csv_without_transcript(CLEANED_MIDDLE_CSV, MIDDLE)
    write_csv_without_transcript(CLEANED_UNPOPULAR_CSV, UNPOPULAR)
    write_pickle(CLEANED_POPULAR_PICKLE, POPULAR)
    write_pickle(CLEANED_MIDDLE_PICKLE, MIDDLE)
    write_pickle(CLEANED_UNPOPULAR_PICKLE, UNPOPULAR)

    print('\ncleaned popular:', len(process_pickle(CLEANED_POPULAR_PICKLE)))
    print('cleaned middle:', len(process_pickle(CLEANED_MIDDLE_PICKLE)))
    print('cleaned unpopular:', len(process_pickle(CLEANED_UNPOPULAR_PICKLE)))

    """ reality check """

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
