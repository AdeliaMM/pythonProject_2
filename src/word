from bs4 import BeautifulSoup
from requests import get

from random import choice, randrange


def get_word():
    letter = randrange(1, 30)
    print(letter)
    url = 'https://onlinedic.net/ozhegov/letter' + str(letter) + '.php'
    page = get(url)
    page.encoding = page.apparent_encoding
    soup = BeautifulSoup(page.text, "html.parser")
    words = soup.find(class_='words').find_all('li')
    word_tag = choice(words)
    word = str(word_tag.string).lower()
    if word.endswith(('ть', 'ться', 'ый', 'ий', '...')):
        return get_word()
    word_url = word_tag.a['href']
    return word, word_url

def get_meaning(url_end):
    url = 'https://onlinedic.net/ozhegov/' + url_end
    page = get(url)
    page.encoding = page.apparent_encoding
    soup = BeautifulSoup(page.text, "html.parser")
    meaning_tag = soup.find(class_='text')
    meaning = ' '.join(meaning_tag.text.split())
    return meaning
