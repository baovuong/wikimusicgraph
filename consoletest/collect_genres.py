import codecs
import httplib
import json
import locale
import sqlite3
import sys
import urllib
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

def get_wiki_content(page_title):
    arguments = {}
    arguments['action'] = 'query'
    arguments['titles'] = page_title
    arguments['prop'] = 'revisions'
    arguments['rvprop'] = 'content'
    arguments['format'] = 'json'
    url = 'https://en.wikipedia.org/w/api.php?%s' % (urllib.urlencode(arguments))
    
    return json.loads(urllib.urlopen(url).read())

def extract_genre_info_box(text):

    # probably going to use a PDA type of thing
    enclosing_brackets = [] # the stack 



sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

content = get_wiki_content('House_music')
print content['query']['pages'][content['query']['pages'].keys()[0]]['revisions'][0]['*']
