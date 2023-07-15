import os
import pandas as pd
from bs4 import BeautifulSoup as bs

import utils
import config

from typing import List, Tuple, Union

# create table if not exist
if not os.path.isfile(config.words_df_fn):
    df = pd.DataFrame(columns=['words', 'reading', 'translate', 'level', 'id', 'known'])
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


def parse_data(elements: List[str]) -> Tuple[List[str], List[int], List[str]]:
    """ Get all words info """
    readings, levels, translates = [[] for i in range(3)]
    for counter, element in enumerate(elements, start=1):
        word, id_ = element.split(' ')
        url = f'https://www.japandict.com/{word}#entry-{id_}'
        if soup := utils.get_soup(url):
            soup = soup.find('div', attrs={'id': f'entry-{id_}'})
            readings += [get_reading(soup)]
            levels += [get_level(soup)]
            translates += [get_translate(soup)]
    return readings, levels, translates


def get_new_words(elements: List[str]) -> pd.DataFrame:
    """" Get new words dataframe """
    readings, levels, translates = parse_data(elements)
    words, ids = [element.split(' ')[0] for element in elements], [element.split(' ')[1] for element in elements]
    df = pd.DataFrame({'words': words,
                       'reading': readings,
                       'translate': translates,
                       'level': levels,
                       'id': ids})
    df['known'] = ""
    df = df.drop_duplicates(subset=['id']).reset_index(drop=True)
    return df


if __name__ == '__main__':
    kind = 'words'
    chunk_size = 10
    utils.process_new_items(get_new_words, kind, chunk_size=chunk_size)
