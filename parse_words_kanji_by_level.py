import os
import re

import utils
import config
from tqdm import tqdm

from typing import List, NoReturn

collection_def_folder = {'kanjis': config.kanjis_dir, 'words': config.words_dir}
new_data_def_folder = {'kanjis': config.new_kanjis_fn, 'words': config.new_words_fn}


def get_url(level: int, kind: str = 'words') -> str:
    """ Get url from params """
    if kind == 'words':
        return f'https://www.japandict.com/?s=%23jlpt{level}&page='
    elif kind == 'kanjis':
        return f'https://www.japandict.com/kanji/?s=%23jlpt{level}k&page='


def get_items(level: int, kind: str = 'words') -> List[str]:
    """ Parse words or kanjis  """
    pages = list(range(1, config.n_pages[kind][level] + 1))
    def_url = get_url(level, kind=kind)
    items = []
    for counter, page_num in tqdm(enumerate(pages, start=1), total=len(pages), desc=' pages'):
        if soup := utils.get_soup(def_url + str(page_num)):
            all_span = soup.findAll('span', attrs={'class': 'xlarge text-normal me-4'})
            all_a = soup.findAll('a', attrs={'class': 'list-group-item list-group-item-action my-2 mdshadow-1'})
            all_a = [' ' + re.search(r'#entry-(\d+)', a['href']).group(1) for a in all_a] if kind =='words' else ['' for _ in range(len(all_a))]
            if all_span:
                for a, span in zip(all_a, all_span):
                    items.append(f'{span.text}{a}')
    return items


def collect_all(kind: str) -> NoReturn:
    """ Collect levels to single file """
    items = []
    for level in range(5, 0, -1):
        items += utils.read_lines(f'{collection_def_folder[kind]}/n_{level}_jlpt_{kind}.txt')

    print(f'Total {len(items)} {kind} saved as new')
    utils.lines_to_txt(new_data_def_folder[kind], items, mode='w')


def parse_items(kind: str = 'words') -> NoReturn:
    """ Parse and save all items """
    for level in range(5, 0, -1):
        fn = f'{collection_def_folder[kind]}/n_{level}_jlpt_{kind}.txt'
        if not os.path.isfile(fn):
            items = get_items(level, kind=kind)
            print(f"n{level} total {len(items)} {kind}.")
            utils.lines_to_txt(fn, items, mode='w')
        else:
            print(f'N{level} JLPT {kind} already exist.')


kind = 'words'
parse_items(kind)
collect_all(kind)

kind = 'kanjis'
parse_items(kind)
collect_all(kind)
