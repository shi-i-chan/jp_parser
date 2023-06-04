import os
import pandas as pd

import utils
import config

from bs4 import BeautifulSoup as bs
from typing import List, Tuple, Union


# create table if not exist
if not os.path.isfile(config.kanjis_df_fn):
    df = pd.DataFrame(columns=['kanjis', 'meaning', 'on', 'kun', 'nanori',
                               'radicals', 'rad nums', 'pop words', 'level', 'known'])
    df.to_excel(config.kanjis_df_fn)


def get_level(kanji: str) -> int:  # so bad
    """ Get current kanji level """
    for level in range(1, 6):
        kanjis = utils.read_lines(f'{config.kanjis_dir}/n_{level}_jlpt_kanjis.txt')
        if kanji in kanjis:
            return level
    return 10


def get_readings(soup: bs, show_errors: bool = False) -> Tuple[List[str], List[str], List[str]]:
    """ Get current kanji readings """
    dl_s = soup.findAll('dl', attrs={'class': 'm-0'})
    on_s, kun_s, nanori = [[] for _ in range(3)]

    mirror = {"On'yomi": on_s, "Kun'yomi": kun_s, 'Nanori': nanori}
    for dl in dl_s:
        dt = dl.findAll('dt')
        try:
            spans = dl.findAll('span', attrs={'class': 'me-4'})
            for span in spans:
                mirror[dt[0].text].append(span.text)
        except Exception as e:
            if show_errors: print(e)
    return on_s, kun_s, nanori


def get_meaning(soup: bs) -> Union[str, bool]:
    """ Get current kanji meaning """
    if meaning := soup.findAll('li', attrs={'class': 'list-group-item p-3'}):
        return meaning[1].text
    return False


def get_radicals(soup: bs, show_errors: bool = False) -> Tuple[List[str], List[int]]:
    """ Get current kanji radicals """
    radicals, radical_numbers = [[] for _ in range(2)]
    try:
        if radicals_div := soup.find('div', attrs={'class': 'card-body d-flex flex-row flex-wrap'}):
            items = radicals_div.findAll('div', attrs={'class': 'd-flex flex-column align-items-center'})
            for item in items:
                radical_div = item.find('div', attrs={'class': 'big mb-auto radical_font'})
                radical = radical_div.text

                radical_number_div = item.find('div', attrs={'class': 'small text-muted'})
                radical_number = radical_number_div.text.strip().replace('Radical #', '')

                radicals.append(radical)
                radical_numbers.append(radical_number)
    except Exception as e:
        if show_errors: print(e)
    return radicals, radical_numbers


def get_popular_words(soup: bs) -> List[str]:
    """ Get popular words with current kanji """
    popular_words = []
    if divs := soup.findAll('div', attrs={'class': 'd-inline-block text-truncate w-100 text-muted'}):
        for div in divs:
            span = div.find('span', attrs={'class': 'xlarge me-4 text-normal radical_font'})
            popular_words.append(span.text)
    else:
        popular_words.append('')
    return popular_words


def parse_data(kanjis: List[str]) -> Tuple[List[str], ...]:
    """ Get all kanji info """
    def_url = 'https://www.japandict.com/kanji/'
    meanings, readings, radicals, levels, popular_words = [[] for _ in range(5)]
    for counter, kanji in enumerate(kanjis, start=1):
        if soup := utils.get_soup(def_url + kanji):
            meanings += [get_meaning(soup)]
            readings += [get_readings(soup)]
            radicals += [get_radicals(soup)]
            levels += [get_level(kanji)]
            popular_words += [get_popular_words(soup)]
    return meanings, readings, radicals, levels, popular_words


def get_new_kanjis(new_kanjis: List[str]) -> pd.DataFrame:
    """ Get new kanjis dataframe """
    meanings, readings, radicals, levels, popular_words = parse_data(new_kanjis)
    df = pd.DataFrame({'kanji': new_kanjis,
                       'meaning': meanings,
                       'on': [", ".join(reading[0]) for reading in readings],
                       'kun': [", ".join(reading[1]) for reading in readings],
                       'nanori': [", ".join(reading[2]) for reading in readings],
                       'radicals': [", ".join(radicals_data[0]) for radicals_data in radicals],
                       'rad nums': [", ".join(radicals_data[1]) for radicals_data in radicals],
                       'pop words': [", ".join(words) for words in popular_words],
                       'level': levels
                       })
    df['known'] = ""
    return df


if __name__ == '__main__':
    kind = 'kanjis'
    chunk_size = 10
    utils.process_new_items(get_new_kanjis, kind, chunk_size=chunk_size)
