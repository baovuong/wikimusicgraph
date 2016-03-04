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
        '{':       [ (1,'Z',''),(2,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(22,'a',''),(21,'a','a'),(),() ],
        '}':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(23,'a',''),(),(21,'a','~'),() ],
        'I':       [ (),(),(3,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'n':       [ (),(),(),(4,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(19,'Z',''),(),(),(21,'a',''),(),(),() ],
        'f':       [ (),(),(),(),(5,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'o':       [ (),(),(),(),(),(6,'Z',''),(),(8,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'b':       [ (),(),(),(),(),(),(7,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'x':       [ (),(),(),(),(),(),(),(),(9,'Z',''),(),(),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'm':       [ (),(),(),(),(),(),(),(),(),(),(11,'Z',''),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'u':       [ (),(),(),(),(),(),(),(),(),(),(),(12,'Z',''),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        's':       [ (),(),(),(),(),(),(),(),(),(),(),(),(13,'Z',''),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'i':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(14,'Z',''),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'c':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(15,'Z',''),(),(),(),(),(),(),(21,'a',''),(),(),() ],
        'g':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(17,'Z',''),(),(),(),(),(21,'a',''),(),(),() ],
        'e':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(18,'Z',''),(),(),(21,'Z','a'),(21,'a',''),(),(),() ],
        'r':       [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(20,'Z',''),(),(21,'a',''),(),(),() ],
        ' ':       [ (),(),(),(),(),(),(),(),(),(10,'Z',''),(),(),(),(),(),(16,'Z',''),(),(),(),(),(),(21,'a',''),(),(),() ],
        'default': [ (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(21,'a',''),(),(),() ],
    }
    state_stack = ['Z']
    
    for character in text:

        step = state_transitions[character][current_state] if character in state_transitions else state_transitions['default'][current_state]
        if len(step) != 3:
            # dead. try again
            current_state = 0
            state_stack = ['Z']
            output = ''
            
        elif step[1] != state_stack[-1]:
            # dead. try again
            current_state = 0
            state_stack = ['Z']
            output = ''
        
        else:
            # do the step
            #print state_stack, current_state
            output += character
            current_state = step[0]
            if step[2] != '':
                if step[2] == '~':
                    #print 'poppin'
                    state_stack.pop()
                else:
                    state_stack.append(step[2])
        #print output 
        if state_stack[-1] == 'Z' and current_state == 21:
            #print 'done'
            break

    return output

def infobox_to_music_genre(infobox_text):
    pass 

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

content = get_wiki_content('House_music')
text = content['query']['pages'][content['query']['pages'].keys()[0]]['revisions'][0]['*']
print extract_genre_info_box(text)
