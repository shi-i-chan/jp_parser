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


def get_new_items(kind: str) -> List[str]:
    """ Get new kanjis """
    new_items = read_lines(getattr(config, f'new_{kind}_fn'))
    exist_items = pd.read_excel(getattr(config, f'{kind}_df_fn'), index_col=0)[kind].tolist()
    new_items = [new_item for new_item in new_items if new_item not in exist_items]
    return new_items


def update_df(new_df: pd.DataFrame, kind: str) -> NoReturn:
    """ Save new rows to df """
    if new_df.shape[0] != 0:
        old_df = pd.read_excel(getattr(config, f'{kind}_df_fn'), index_col=0)
        new_df = pd.concat([old_df, new_df])
        new_df = new_df.sort_values(by=['known', 'level'],
                                    ascending=[True, False]).drop_duplicates().reset_index(drop=True)
        new_df.to_excel(getattr(config, f'{kind}_df_fn'))


def process_new_items(func: Callable, kind: str, chunk_size: int = 10) -> NoReturn:
    new_items = get_new_items(kind)
    if new_items:
        chunks = np.array_split(new_items, math.ceil(len(new_items) / chunk_size))
        for chunk in tqdm(chunks, total=len(chunks), desc=' chunks'):
            new_df = func(chunk)
            update_df(new_df, kind)
