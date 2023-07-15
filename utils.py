import math
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

import config

from typing import Union, List, NoReturn, Callable
from requests import Response


def get_html(url: str) -> Union[Response, bool]:
    """ Get html from url """
    with requests.Session() as s:
        page_html = s.get(url, headers=config.headers)
    if page_html.status_code == 200:
        return page_html
    return False


def get_soup(url: str) -> Union[bs, bool]:
    """ Get soup from url """
    if page_html := get_html(url):
        soup = bs(page_html.text, 'html.parser')
        return soup
    return False


def read_lines(fn: str) -> List:
    with open(fn, 'r', encoding='utf-8') as f:
        txt_words = f.read().splitlines()
    return txt_words


def lines_to_txt(fn: str, new_lines: List[str], mode: str = 'a') -> NoReturn:
    with open(fn, mode, encoding='utf-8') as f:
        f.writelines("\n".join(new_lines))
        f.write("\n")


def get_new_words():
    new_lines = read_lines(getattr(config, f'new_words_fn'))
    new_items = [new_line.split(' ')[0] for new_line in new_lines]
    new_ids = [new_line.split(' ')[1] for new_line in new_lines]
    exist_ids = pd.read_excel(getattr(config, f'words_df_fn'), index_col=0)['id'].tolist()
    new_items_indices = []
    for i in range(len(new_ids)):
        if new_ids[i] not in exist_ids:
            new_items_indices.append(i)
    return [new_lines[i] for i in new_items_indices]


def get_new_kanjis() -> List[str]:
    """ Get new kanjis """
    new_items = read_lines(getattr(config, f'new_kanjis_fn'))
    exist_items = pd.read_excel(getattr(config, f'kanjis_df_fn'), index_col=0)[kind].tolist()
    new_items = [new_item for new_item in new_items if new_item not in exist_items]
    return new_items


def update_df(new_df: pd.DataFrame, kind: str) -> NoReturn:
    """ Save new rows to df """
    if new_df.shape[0] != 0:
        old_df = pd.read_excel(getattr(config, f'{kind}_df_fn'), index_col=0)
        new_df = pd.concat([old_df, new_df])
        new_df = new_df.sort_values(by=['known', 'level'],
                                    ascending=[True, False]).reset_index(drop=True)
        new_df.to_excel(getattr(config, f'{kind}_df_fn'))


def process_new_items(func: Callable, kind: str, chunk_size: int = 10) -> NoReturn:
    mirror = {'words': get_new_words, 'kanjis': get_new_kanjis}
    new_items = mirror[kind]()
    if new_items:
        chunks = np.array_split(new_items, math.ceil(len(new_items) / chunk_size))
        for chunk in tqdm(chunks, total=len(chunks), desc=' chunks'):
            new_df = func(chunk)
            update_df(new_df, kind)
