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

    # there should be 25 states. 0 - 24
    # each output of the state transition will be a 3 value tuple: (next state,what's on top of the stack,what to replace top of stack with)
    current_state = 0
    state_transitions = {
        '{':       [ (1,'Z',''),(2,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        '}':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'I':       [ (),(),(3,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'n':       [ (),(),(),(4,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(19,'Z',''),(),(),(),(),(),() ],
        'f':       [ (),(),(),(),(5,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'o':       [ (),(),(),(),(),(6,'Z',''),(),(8,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'b':       [ (),(),(),(),(),(),(7,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'x':       [ (),(),(),(),(),(),(),(),(9,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'm':       [ (),(),(),(),(),(),(),(),(),(),(11,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        'u':       [ (),(),(),(),(),(),(),(),(),(),(),(12,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),() ],
        's':       [ (),(),(),(),(),(),(),(),(),(),(),(),(13,'Z',''),(),(),(),(),(),(),(),(),(),(),(),() ],
        'i':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(14,'Z',''),(),(),(),(),(),(),(),(),(),(),() ],
        'c':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(15,'Z',''),(),(),(),(),(),(),(),(),(),() ],
        'g':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(17,'Z',''),(),(),(),(),(),(),(),() ],
        'e':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(18,'Z',''),(),(),(21,'Z','a'),(),(),(),() ],
        'r':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(20,'Z',''),(),(),(),(),() ],
        ' ':       [ (),(),(),(),(),(),(),(),(),(10,'Z',''),(),(),(),(),(),(16,'Z',''),(),(),(),(),(),(),(),(),() ],
        'default': [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),() ],
    }
    state_stack = ['Z']



sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

content = get_wiki_content('House_music')
text = content['query']['pages'][content['query']['pages'].keys()[0]]['revisions'][0]['*']
print text
