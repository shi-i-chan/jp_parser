# jp_parser

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
