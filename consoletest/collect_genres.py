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
    entry = ''
    assignment_index = ''
    state = 0
    steps = []
    saved_state = 0

    for character in infobox_text:
        steps.append((state,character))
        if state == 0:
            if character.lower()== '|':
                entry = ''
                assignment_index = ''
                state = 1
            continue
            
        if state == 1:
            if character.lower() == 'f':
                state = 40
            elif character.lower()== 'd':
                state = 29
            elif character.lower()== 's':
                state = 7
            elif character.lower()== 'n':
                state = 2
            elif character.lower()== ' ':
                state = 1
            else:
                state = 0
            continue
            
        if state == 2:
            if character.lower()== 'a':
                state = 3
            else:
                state = 0
            continue
            
        if state == 3:
            if character.lower()== 'm':
                state = 4
            else:
                state = 0
            continue
            
        if state == 4:
            if character.lower()== 'e':
                state = 5
            else:
                state = 0
            continue
            
        if state == 5:
            if character.lower()== '=':
                state = 6
            elif character.lower()== ' ':
                state = 5
            else:
                state = 0
            continue
            
        if state == 6:
            if character.lower()== '|':
                state = 1
            else:
                # extract stuff
                genre_name += character
            continue
            
        if state == 7:
            if character.lower()== 't':
                state = 8
            elif character.lower()== 'u':
                state = 52
            else:
                state = 0
            continue
            
        if state == 8:
            if character.lower()== 'y':
                state = 9
            else:
                state = 0
            continue
            
        if state == 9:
            if character.lower()== 'l':
                state = 10
            else:
                state = 0
            continue
            
        if state == 10:
            if character.lower()== 'i':
                state = 11
            else:
                state = 0
            continue
            
        if state == 11:
            if character.lower()== 's':
                state = 12
            else:
                state = 0
            continue
            
        if state == 12:
            if character.lower()== 't':
                state = 13
            else:
                state = 0
            continue
            
        if state == 13:
            if character.lower()== 'i':
                state = 14
            else:
                state = 0
            continue
        
        if state == 14:
            if character.lower()== 'c':
                state = 15
            else:
                state = 0
            continue
        
        if state == 15:
            if character.lower()== '_':
                state = 16
            else:
                state = 0
            continue
            
        if state == 16:
            if character.lower()== 'o':
                state = 17
            else:
                state = 0
            continue
            
        if state == 17:
            if character.lower()== 'r':
                state = 18
            else:
                state = 0
            continue
            
        if state == 18:
            if character.lower()== 'i':
                state = 19
            else:
                state = 0
            continue
            
        if state == 19:
            if character.lower()== 'g':
                state = 20
            else:
                state = 0
            continue
            
        if state == 20:
            if character.lower()== 'i':
                state = 21
            else:
                state = 0
            continue
            
        if state == 21:
            if character.lower()== 'n':
                state = 22
            else:
                state = 0
            continue
            
        if state == 22:
            if character.lower()== 's':
                state = 23
            else:
                state = 0
            continue
            
        if state == 23:
            if character.lower()== '=':
                # do the thing
                assignment_index = 'stylistic_origins'
                print assignment_index
                state = 24
            elif character.lower()== ' ':
                state = 23
            else:
                state = 0
            continue
            
        if state == 24:
            #print assignment_index
            if character.lower()== '{':
                #print 'inside curly'
                state = 25
            elif character.lower()== '[':
                saved_state = 24
                state = 26
            elif character.lower()== '|':
                state = 1
                # reset, start anew
            elif character.lower()== '<':
                saved_state = 24
                state = 60
            else:
                state = 24
            continue
            
        if state == 25:
            if character.lower()== '[':
                saved_state = 25
                state = 26
            elif character.lower()== '}':
                #print 'outside curly'
                state = 24
            elif character.lower()== '<':
                saved_state = 25
                state = 60
            else:
                state = 25
            continue
            
        if state == 26:
            if character.lower()== '[':
                # start the extraction
                entry = ''
                state = 27
            else:
                state = 25
            continue
            
        if state == 27:
            # woo extraction 
            if character.lower()== ']':
                # don't extract this part
                state = 28
            else:
                # extract pls
                entry += character
                state = 27
            continue
            
        if state == 28:
            if character.lower()== ']':
                # close it up and save it
                #print entry
                assignment[assignment_index].append(entry)
                state = saved_state
            else:
                # extract character
                entry += character
                state = 27
            continue
            
        if state == 29:
            if character.lower()== 'e':
                state = 30
            else:
                state = 0
            continue
            
        if state == 30:
            if character.lower()== 'r':
                state = 31
            else:
                state = 0
            continue
            
        if state == 31:
            if character.lower()== 'i':
                state = 32
            else:
                state = 0
            continue
            
        if state == 32:
            if character.lower()== 'v':
                state = 33
            else:
                state = 0
            continue
            
        if state == 33:
            if character.lower()== 'a':
                state = 34
            else:
                state = 0
            continue
            
        if state == 34:
            if character.lower()== 't':
                state = 35
            else:
                state = 0
            continue
        
        if state == 35:
            if character.lower()== 'i':
                state = 36
            else:
                state = 0
            continue
            
        if state == 36:
            if character.lower()== 'v':
                state = 37
            else:
                state = 0
            continue
            
        if state == 37:
            if character.lower()== 'e':
                state = 38
            else:
                state = 0
            continue
            
        if state == 38:
            if character.lower()== 's':
                state = 39
            else:
                state = 0
            continue
            
        if state == 39:
            if character.lower()== '=':
                assignment_index = 'derivative_forms'
                state = 24
            elif character.lower()== ' ':
                state = 39
            else:
                state = 0
            continue
            
        if state == 40:
            if character.lower()== 'u':
                state = 41
            else:
                state = 0
            continue
            
        if state == 41:
            if character.lower()== 's':
                state = 42
            else:
                state = 0
            continue
            
        if state == 42:
            if character.lower()== 'i':
                state = 43
            else:
                state = 0
            continue
            
        if state == 43:
            if character.lower()== 'o':
                state = 44
            else:
                state = 0
            continue
            
        if state == 44:
            if character.lower()== 'n':
                state = 45
            else:
                state = 0
            continue
            
        if state == 45:
            if character.lower()== 'g':
                state = 46
            else:
                state = 0
            continue
            
        if state == 46:
            if character.lower()== 'e':
                state = 47
            else:
                state = 0
            continue
            
        if state == 47:
            if character.lower()== 'n':
                state = 48
            else:
                state = 0
            continue
            
        if state == 48:
            if character.lower()== 'r':
                state = 49
            else:
                state = 0
            continue
        
        if state == 49:
            if character.lower()== 'e':
                state = 50
            else:
                state = 0
            continue
            
        if state == 50:
            if character.lower()== 's':
                state = 51
            else:
                state = 52
            continue
            
        if state == 51:
            if character.lower()== '=':
                assignment_index = 'fusion_genres'
                state = 24
            elif character.lower()== ' ':
                state = 51
            else:
                state = 0
            continue
            
        if state == 52:
            if character.lower()== 'b':
                state = 53
            else:
                state = 0
            continue
            
        if state == 53:
            if character.lower()== 'g':
                state = 54
            else:
                state = 0
            continue
            
        if state == 54:
            if character.lower()== 'e':
                state = 55
            else:
                state = 0
            continue
            
        if state == 55:
            if character.lower()== 'n':
                state = 56
            else:
                state = 0
            continue
            
        if state == 56:
            if character.lower()== 'r':
                state = 57
            else:
                state = 0
            continue
            
        if state == 57:
            if character.lower()== 'e':
                state = 58
            else:
                state = 0
            continue
            
        if state == 58:
            if character.lower()== 's':
                state = 59
            else:
                state = 0
            continue
            
        if state == 59:
            if character.lower()== '=':
                assignment_index = 'subgenres'
                state = 24
            elif character.lower()== ' ':
                state = 59
            else:
                state = 0
            continue
        
        if state == 60:
            if character.lower()== 'r':
                state = 61
            else:
                state = saved_state
            continue
            
        if state == 61:
            if character.lower()== 'e':
                state = 62
            else:
                state = saved_state
            continue
            
        if state == 62:
            if character.lower()== 'f':
                state = 63
            else:
                state = saved_state
            continue
            
        if state == 63:
            if character.lower()== '>':
                state = 64
            elif character.lower()== ' ':
                state = 70
            elif character.lower()== '/':
                state = 69
            else:
                state = saved_state
            continue
            
        if state == 64:
            if character.lower()== '<':
                state = 65
            else:
                state = 64
            continue
            
        if state == 65:
            if character.lower()== '/':
                state = 66
            else:
                state = 64
            continue
            
        if state == 66:
            if character.lower()== 'r':
                state = 67
            else:
                state = 64
            continue
            
        if state == 67:
            if character.lower()== 'e':
                state = 68
            else:
                state = 64
            continue
            
        if state == 68:
            if character.lower()== 'f':
                state = 69
            else:
                state = 64
            continue
            
        if state == 69:
            if character.lower()== '>':
                state = saved_state
            else:
                state = 64
            continue
            
        if state == 70:
            if character.lower()== '>':
                state = 64
            elif character.lower()== '/':
                state = 69
            else:
                state = 70
            continue
    # ok, got the info. let's put them together
    #print steps
    genre = MusicGenre(genre_name,'','')
    genre.fusion_genres = assignment['fusion_genres']
    genre.subgenres = assignment['subgenres']
    genre.derivative_forms = assignment['derivative_forms']
    genre.stylistic_origins = assignment['stylistic_origins']
    
    return genre

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

search_input = raw_input('genre name: ')

content = get_wiki_content(search_input)
text = content['query']['pages'][content['query']['pages'].keys()[0]]['revisions'][0]['*']
infobox = extract_genre_info_box(text)
genre = infobox_to_music_genre(infobox)
print 'name:',genre.genre
print 'subgenres:'
for g in genre.subgenres:
    print '*',g
print 'stylistic origins:'
for g in genre.stylistic_origins:
    print '*',g
print 'fusion genres:'
for g in genre.fusion_genres:
    print '*',g
print 'derivative forms'
for g in genre.derivative_forms:
    print '*',g

