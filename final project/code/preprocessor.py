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

# csv's
UNCLEANED_POPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/uncleaned_popular.csv'
UNCLEANED_MIDDLE_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/uncleaned_middle.csv'
UNCLEANED_UNPOPULAR_CSV = 'C:/Users/Noa/Desktop/huji/second year/dataMining/final project/output/uncleaned_unpopular.csv'
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


def create_df(lst, columns):
    """ creates df without transcript """
    return pd.DataFrame(
        [[getattr(i, j) for j in columns] for i in lst],
        columns=columns)


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


def data_clean(popular, middle, unpopular):
    # write uncleaned csv
    write_csv_without_transcript(UNCLEANED_POPULAR_CSV, popular)
    write_csv_without_transcript(UNCLEANED_MIDDLE_CSV, middle)
    write_csv_without_transcript(UNCLEANED_UNPOPULAR_CSV, unpopular)

    # POPULAR
    print('POPULAR\noriginal: ', len(popular))
    popular = remove_talks_without_transcript(popular)
    print('transcript:', len(popular))
    popular = remove_talks_with_missing_values(popular)
    print('values:', len(popular))

    # MIDDLE
    print('\nMIDDLE\noriginal: ', len(middle))
    middle = remove_talks_without_transcript(middle)
    print('transcript:', len(middle))
    middle = remove_talks_with_missing_values(middle)
    print('values:', len(middle))

    # UNPOPULAR
    print('\nUNPOPUAR\noriginal: ', len(unpopular))
    unpopular = remove_talks_without_transcript(unpopular)
    print('transcript:', len(unpopular))
    unpopular = remove_talks_with_missing_values(unpopular)
    print('values:', len(unpopular))

    # export to CSV without transcript
    write_csv_without_transcript(CLEANED_POPULAR_CSV, popular)
    write_csv_without_transcript(CLEANED_MIDDLE_CSV, middle)
    write_csv_without_transcript(CLEANED_UNPOPULAR_CSV, unpopular)

    # export to pickle
    write_pickle(CLEANED_POPULAR_PICKLE, popular)
    write_pickle(CLEANED_MIDDLE_PICKLE, middle)
    write_pickle(CLEANED_UNPOPULAR_PICKLE, unpopular)

    print('\ncleaned popular:', len(process_pickle(CLEANED_POPULAR_PICKLE)))
    print('cleaned middle:', len(process_pickle(CLEANED_MIDDLE_PICKLE)))
    print('cleaned unpopular:', len(process_pickle(CLEANED_UNPOPULAR_PICKLE)))

    return popular, middle, unpopular


def reality_check(popular, middle, unpopular):
    pass


if __name__ == '__main__':
    uncleaned_popular = process_pickle(POPULAR_PICKLE)
    uncleaned_middle = process_pickle(MIDDLE_PICKLE)
    uncleaned_unpopular = process_pickle(UNPOPULAR_PICKLE)

    """ data cleaning """
    cleaned_popular, cleaned_middle, cleaned_unpopular = data_clean(
        uncleaned_popular, uncleaned_middle, uncleaned_unpopular)

    """ reality check """
    reality_check(uncleaned_popular, uncleaned_middle, uncleaned_unpopular)
    reality_check(cleaned_popular, cleaned_middle, cleaned_unpopular)

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
