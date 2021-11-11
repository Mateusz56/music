import requests
import random
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()
for i, WORD in enumerate(WORDS):
    WORDS[i] = str(WORD)[2: -1]

from song.models import Song
print(random.choice(Song.Genres.choices))


def generate_songs():
    from song.models import Song

    for i in range(0, 100):
        performer = random.choice(WORDS)
        for j in range(0, 20):
            s = Song(title=random.choice(WORDS), performer=performer, year=random.randint(1900, 2020), genre = random.choice(Song.Genres.choices[0]))
            s.save()
