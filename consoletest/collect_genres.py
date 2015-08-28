import sqlite3
import wikipedia

class MusicGenre:
    def __init__(self,genre,summary,wiki_link):
        self.genre = genre
        self.summary = summary
        self.wiki_link = wiki_link
        self.subgenres = []
        self.fusion_genres = []
        self.derivative_forms = []
        self.stylistic_origins = []


anti_folk = wikipedia.page('Anti-folk')
print anti_folk.html()
