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
    # I will probably do the same thing. just FSM my way to this. technically the most efficient route
    genre_name = ''
    assignment = {
        'stylistic_origins': [],
        'subgenres': [],
        'derivative_forms': [],
        'fusion_genres': []
    }
    assignment_index = ''
    state = 0
    transitions = [
    ]

    for character in infobox_text:
        if state == 0:
            if character == '|':
                state = 1
            continue
            
        if state == 1:
            if character == 'f':
                state = 40
            elif character == 'd':
                state = 29
            elif character == 's':
                state = 7
            elif character == 'n':
                state = 2
            else:
                state = 0
            continue
            
        if state == 2:
            if character == 'a':
                state = 3
            else:
                state = 0
            continue
            
        if state == 3:
            if character == 'm':
                state = 4
            else:
                state = 0
            continue
            
        if state == 4:
            if character == 'e':
                state = 5
            else:
                state = 0
            continue
            
        if state == 5:
            if character == '=':
                state = 6
            elif character == ' ':
                state = 5
            else:
                state = 0
            continue
            
        if state == 6:
            if character == '|':
                state = 1
            else:
                # extract stuff
                genre_name += character
            continue
            
        if state == 7:
            if character == 't':
                state = 8
            elif character == 'u':
                state = 52
            else:
                state = 0
            continue
            
        if state == 8:
            if character == 'y':
                state = 9
            else:
                state = 0
            continue
            
        if state == 9:
            if character == 'l':
                state = 10
            else:
                state = 0
            continue
            
        if state == 10:
            if character == 'i':
                state = 11
            else:
                state = 0
            continue
            
        if state == 11:
            if character == 's':
                state = 12
            else:
                state = 0
            continue
            
        if state == 12:
            if character == 't':
                state = 13
            else:
                state = 0
            continue
            
        if state == 13:
            if character == 'i':
                state = 14
            else:
                state = 0
            continue
        
        if state == 14:
            if character == 'c':
                state = 15
            else:
                state = 0
            continue
        
        if state == 15:
            if character == '_':
                state == 16
            else:
                state = 0
            continue
            
        if state == 16:
            if character == 'o':
                state = 17
            else:
                state = 0
            continue
            
        if state == 17:
            if character == 'r':
                state = 18
            else:
                state = 0
            continue
            
        if state == 18:
            if character == 'i':
                state = 19
            else:
                state = 0
            continue
            
        if state == 19:
            if character == 'g':
                state = 20
            else:
                state = 0
            continue
            
        if state == 20:
            if character == 'i':
                state = 21
            else:
                state = 0
            continue
            
        if state == 21:
            if character == 'n':
                state = 22
            else:
                state = 0
            continue
            
        if state == 22:
            if character == 's':
                state = 23
            else:
                state = 0
            continue
            
        if state == 23:
            if character == '=':
                # do the thing
                assignment_index = 'stylistic_origins'
                state = 24
            elif character == ' ':
                state = 23
            else:
                state = 0
            continue
            
        if state == 24:
            if character == '{':
                state = 25
            elif character == '[':
                state = 26
            elif character == '|':
                state = 1
                # reset, start anew
            else:
                state = 24
            continue
            
        if state == 25:
            if character == '[':
                state = 26
            elif character == '}':
                state = 24
            else:
                state = 25
            continue
            
        if state == 26:
            if character == '[':
                # start the extraction
                state = 27
            else:
                state = 25
            continue
            
        if state == 27:
            # woo extraction 
            if character == ']':
                # don't extract this part
                state = 28
            else:
                # extract pls
                state = 27
            continue
            
        if state == 28:
            if character == ']':
                # close it up and save it
                state = 24
            else:
                # extract character
                state = 27
            continue
            
        if (state == 29):
            continue
        if (state == 30):
            continue
        if (state == 31):
            continue
        if (state == 32):
            continue
        if (state == 33):
            continue
        if (state == 34):
            continue
        if (state == 35):
            continue
        if (state == 36):
            continue
        if (state == 37):
            continue
        if (state == 38):
            continue
        if (state == 39):
            continue
        if (state == 40):
            continue
        if (state == 41):
            continue
        if (state == 42):
            continue
        if (state == 43):
            continue
        if (state == 44):
            continue
        if (state == 45):
            continue
        if (state == 46):
            continue
        if (state == 47):
            continue
        if (state == 48):
            continue
        if (state == 49):
            continue
        if (state == 50):
            continue
        if (state == 51):
            continue
        if (state == 52):
            continue
        if (state == 53):
            continue
        if (state == 54):
            continue
        if (state == 55):
            continue
        if (state == 56):
            continue
        if (state == 57):
            continue
        if (state == 58):
            continue
        if (state == 59):
            continue
        if (state == 60):
            continue
        if (state == 61):
            continue

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

content = get_wiki_content('Downtempo')
text = content['query']['pages'][content['query']['pages'].keys()[0]]['revisions'][0]['*']
print extract_genre_info_box(text)
