import os
import pandas as pd
from bs4 import BeautifulSoup as bs

import utils
import config

from typing import List, Tuple, Union

# create table if not exist
if not os.path.isfile(config.words_df_fn):
    df = pd.DataFrame(columns=['words', 'reading', 'translate', 'level', 'known'])
    df.to_excel(config.words_df_fn)


def get_level(soup: bs) -> int:  # so bad
    """ Get current word level """
    if level_span := soup.find('span', attrs={'class': 'badge me-1 bg-darkorange'}):
        level = int(level_span.text[-1])
        return level
    return 10


def get_reading(soup: bs) -> Union[str, bool]:
    """ Get current word readings """
    reading_div = soup.find('div', attrs={'class': 'd-flex justify-content-between align-items-center'})
    if reading_div:
        reading_spans = reading_div.findAll('span')
        reading = []
        for span in reading_spans:
            reading.append(span.text.strip())
        return "".join(reading)
    return False


def get_translate(soup: bs) -> str:
    """ Get current word translates """
    translate_divs = soup.findAll('div', attrs={'lang': 'en'})
    translates = []
    for div in translate_divs:
        translates.append(div.text.strip())
    translates = " | ".join(translates)
    return translates


def parse_data(words: List[str]) -> Tuple[List[str], List[int], List[str]]:
    """ Get all words info """
    link = 'https://www.japandict.com/'
    readings, levels, translates = [[] for i in range(3)]
    for counter, word in enumerate(words, start=1):
        if soup := utils.get_soup(link + word):
            readings += [get_reading(soup)]
            levels += [get_level(soup)]
            translates += [get_translate(soup)]
    return readings, levels, translates


def get_new_words(new_words: List[str]) -> pd.DataFrame:
    """" Get new words dataframe """
    readings, levels, translates = parse_data(new_words)
    df = pd.DataFrame({'words': new_words,
                       'reading': readings,
                       'translate': translates,
                       'level': levels})
    df['known'] = ""
    return df


if __name__ == '__main__':
    kind = 'words'
    chunk_size = 10
    utils.process_new_items(get_new_words, kind, chunk_size=chunk_size)
