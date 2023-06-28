# jp_parser

<details open>
<summary>
ENG readme
</summary>

<ul>

With this parser, you can collect some data from the site https://www.japandict.com, namely:
1. Lists of all words by JLPT levels are stored in the folder `japanese_word_kanji_parser\data\words by jlpt lvl`.

2. Lists of all hieroglyphs by JLPT levels are stored in the folder `japanese_word_kanji_parser\data\kanjis by jlpt lvl`.

3. Table with all radicals.

4. Table with all JLPT characters.

5. Table with all JLPT words.

## Defects:
- Parallel execution is not implemented, so the parser is very slow.
- When getting word data, there are problems with getting katakana or no tone showing readings.

## Usage:
1. Run file `japanese_word_kanji_parser\parse_words_kanji_by_level.py`.

<ul>

Text files with lists of words and hieroglyphs, as well as these lists separately by JLPT levels will appear in folder `japanese_word_kanji_parser\data`.

</ul>
  
2. Run file `japanese_word_kanji_parser\new_kanji_processing.py`.

<ul>

File `kanji_df.xlsx` will appear in folder `japanese_word_kanji_parser\table`.

![image](https://github.com/shi-i-chan/jp_parser/blob/main/screens/kanjis_df.png)

</ul>

3. Run file `japanese_word_kanji_parser\new_words_processing.py`.

<ul>

File `words_df.xlsx` will appear in folder `japanese_word_kanji_parser\table`.

![image](https://github.com/shi-i-chan/jp_parser/blob/main/screens/words_df.png)

</ul>

4. Run file `japanese_word_kanji_parser\get_all_radicals.py`.

<ul>

File `radicals.xlsx` will appear in folder `japanese_word_kanji_parser\table`.

![image](https://github.com/shi-i-chan/jp_parser/blob/main/screens/radicals.png)

</ul>

<ul>

</details>

<details>
<summary>
RU readme
</summary>

<ul>

С помощью этого парсера можно собрать некоторые данные с сайта https://www.japandict.com, а именно:
1. Списки всех японских слов по уровням JLPT находятся в папке `japanese_word_kanji_parser\data\words by jlpt lvl`.

2. Списки всех иероглифов по уровням JLPT находятся в папке `japanese_word_kanji_parser\data\kanjis by jlpt lvl`.

3. Таблицу со всеми радикалами.

4. Таблицу со всеми иероглифами по уровням JLPT.

5. Таблицу со всеми японскими словами по уровням JLPT.

## Недостатки:
- Не реализовано параллельное выполнение, так что парсер работает медленно.
- При сборе данных есть некоторые проблемы с получением чтений на катакане или чтений без отображения тона чтения. и When getting word data, there are problems with getting katakana or no tone showing readings.

## Использование:
1. Запустить файл `japanese_word_kanji_parser\parse_words_kanji_by_level.py`.

<ul>

Текстовые файлы со списками всех слов и иероглифов, а также их списки по уровням JLPT появятся в папке `japanese_word_kanji_parser\data`.

</ul>
  
2. Запустить файл `japanese_word_kanji_parser\new_kanji_processing.py`.

<ul>

Файл `kanji_df.xlsx` появится в папке `japanese_word_kanji_parser\table`.

![image](https://github.com/shi-i-chan/jp_parser/blob/main/screens/kanjis_df.png)

</ul>

3. Запустить файл `japanese_word_kanji_parser\new_words_processing.py`.

<ul>

Файл `words_df.xlsx` появится в папке `japanese_word_kanji_parser\table`.

![image](https://github.com/shi-i-chan/jp_parser/blob/main/screens/words_df.png)

</ul>

4. Запустить файл `japanese_word_kanji_parser\get_all_radicals.py`.

<ul>

Файл `radicals.xlsx` появится в папке `japanese_word_kanji_parser\table`.

![image](https://github.com/shi-i-chan/jp_parser/blob/main/screens/radicals.png)

</ul>

</details>
