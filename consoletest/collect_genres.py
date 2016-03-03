import codecs
import httplib
import json
import locale
import sqlite3
import sys
import urllib
#import wikipedia

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
    output = ''
    # probably going to use a PDA type of thing
    enclosing_brackets = [] # the stack 
    state = 0
    for c in text:
        if state == 0:
            continue
        if state == 1:
            continue
        if state == 2:
            continue
        if state == 3:
            continue
        if state == 4:
            continue
        if state == 5:
            continue
        if state == 6:
            continue
        if state == 7:
            continue        
        if state == 8:
            continue
        if state == 9:
            continue
        if state == 10:
            continue
        if state == 11:
            continue
        if state == 12:
            continue
        if state == 13:
            continue
        if state == 14:
            continue
        if state == 15:
            continue
        if state == 16:
            continue
        if state == 17:
            continue 
        if state == 18:
            continue
        if state == 19:
            continue
        if state == 20:
            continue
        if state == 21:
            continue
        if state == 22:
            continue
        if state == 23:
            continue
        if state == 24:
            continue
        pass 
    
    
    return output;
    



sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

content = get_wiki_content('House_music')
print content['query']['pages'][content['query']['pages'].keys()[0]]['revisions'][0]['*']
