from bs4 import BeautifulSoup
from requests import get
from re import sub

from random import choice


def get_word():
  letters = list(range(192, 223))
  letters = letters[:27] + letters[30:]
  letter = choice(letters)
  url = 'https://slovarozhegova.ru/letter.php?charkod=' + str(letter)
  page = get(url)
  page.encoding = page.apparent_encoding
  soup = BeautifulSoup(page.text, "html.parser")
  words = soup.find_all(class_='chara')
  word_tag = choice(words)
  word = 'ё'.join(str(word_tag.string).lower().split())
  word = sub("[^А-Яа-я]", "", word)
  word_url = word_tag.get('href')
  if word.endswith(('ть', 'ться', 'ый', 'ий', '...', '-то', '-либо', '-нибудь')) or 'letter' in word_url:
    return get_word()
  return word, word_url


def get_meaning(url_end):
  url = 'https://slovarozhegova.ru/' + url_end
  page = get(url)
  page.encoding = page.apparent_encoding
  soup = BeautifulSoup(page.text, "html.parser")
  meaning_tag = soup.find(class_='textdiv')
  meaning = ' '.join(meaning_tag.text.split()[1:])
  return meaning
