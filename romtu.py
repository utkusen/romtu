# -*- coding: utf-8 -*-
import re
import random
import string
import operator
from random import choice
from collections import Counter
from lexicon import *
import gensim
import warnings
warnings.filterwarnings("ignore")


print """

██████╗  ██████╗ ███╗   ███╗████████╗██╗   ██╗
██╔══██╗██╔═══██╗████╗ ████║╚══██╔══╝██║   ██║
██████╔╝██║   ██║██╔████╔██║   ██║   ██║   ██║
██╔══██╗██║   ██║██║╚██╔╝██║   ██║   ██║   ██║
██║  ██║╚██████╔╝██║ ╚═╝ ██║   ██║   ╚██████╔╝
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝    ╚═════╝ 
                                              
        Automated Poem Generator
v2 / Utku Sen / Istanbul Bilgi Universitesi                                                                    

"""                              

corpus = gensim.models.KeyedVectors.load_word2vec_format('trcorpus.bin', binary=True)
word_to_similarity = []
similarity_index = {}
translation = {}
notfound = -1 #used for if postag matching is failed.
model_count = 0 #used for counting number of models in a stanza

#compares the similarity of two words and returns an integer value
def similarity_compare(word1, word2):
    u1 = unicode( word1, "utf-8" )
    u2 = unicode( word2, "utf-8" )
    return corpus.similarity(u1, u2)


#searches given word and postag in parsed zemberek wordlist
def find_postag(word,postag):
    with open('zemberekparse.bin',"r") as zemberek: 
        for line in zemberek:
            if word+postag in line:
                if line.split(" ")[0].startswith(word):
                    selectedword = line.split(" ")[0]
                    break
        return selectedword
        

#selects first word randomly, selects other words according to similarity analysis
def select_word(model):
    global notfound
    global model_count

    variable = globals()[model]
    variable.seek(0) 
    lines = variable.read().splitlines()
    most_similar=""
    


    if not word_to_similarity: #if it's the first word select random
        selectedline = random.choice(lines)
        word_to_similarity.append(selectedline)
        most_similar = selectedline
        return  most_similar
    else:

        if notfound != -1: #if postag finding is failed, check for other words in similarity index
            sorted_index = sorted(similarity_index.items(), key=lambda x:x[1], reverse=True)
            most_similar = sorted_index[notfound][0]
            return most_similar

        else:
            for candidate_word in lines:
                try:
                    result = similarity_compare(word_to_similarity[0],candidate_word)
                    similarity_index[candidate_word] = result 

                except:
                    continue            
    
            if len(similarity_index) == 0:
                print "could not find any correlation: ",candidate_word
            else:
                most_similar = choice(Counter(similarity_index).most_common(2))[0] #gets random word from most similar two words
                #most_similar = max(similarity_index.iteritems(), key=operator.itemgetter(1))[0] #gets most similar word

            return most_similar



#returns head of a random pattern with given theme
#added number for now
def find_random_pattern(theme):
    lines = open('poempatterns.txt','r').readlines()
    stripped_lines = map(string.strip, lines)
    found_lines = filter(lambda l: re.match(".*theme=%s.*" % theme, l), stripped_lines)
    return random.choice(found_lines)
    #return found_lines[num]



def create_poem(theme):
    global notfound
    global model_count

    stanza = []
    pattern_head = find_random_pattern(theme)
    duplicate = 0 # a control variable for duplicated words
    for line in pattern:
        if line.rstrip() == pattern_head: #pattern starts
            for line in pattern:
                if line.rstrip() == "</pattern>": #pattern ends
                    break
                word = line.split() 
                for i in range(len(word)):
                    duplicate = 0
                    if word[i] in models: #if the word is noun,pnoun,person etc.
                        model_count += 1
                        try:
                            if word[i+1].startswith('"'): #if a postag definition follows previous word
                                postag = word[i+1][1:-1]
                                
                                try:
                                    selected_word = select_word(word[i])
                                    #print "selected word: ",selected_word

                                except:
                                    continue    
                                result = None
                                while result is None:
                                    try:
                                        final_word = find_postag(selected_word,postag)
                                        result = final_word
                                    except: #if it's cant find postag of given word, looks for a new word
                                        if model_count < 2:
                                            del word_to_similarity[:]
                                            selected_word = select_word(word[i])
                                        else:
                                                
                                            notfound += 1
                                            selected_word = select_word(word[i])
                                        

                                stanza.append(final_word)
                                similarity_index.clear()
                                notfound = -1
                                duplicate = 1
                                
                        except:
                            pass
                        if duplicate == 0:
                            stanza.append(select_word(word[i]))

                    elif word[i].startswith('"'):
                        continue
                    else:
                        stanza.append(word[i])      

                print ' '.join(stanza)
                del stanza[:]
                del word_to_similarity[:]
                similarity_index.clear()
                notfound = -1
                model_count = 0
    
        

create_poem("siir")


