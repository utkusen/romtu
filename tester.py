# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from lexicon import *
from operator import itemgetter
from collections import Counter
from random import choice

model = Word2Vec.load_word2vec_format('trcorpus.bin', binary=True)
similarity_index = {}

def similarity_compare(word1,word2):
	u1 = unicode( word1, "utf-8" )
	u2 = unicode( word2, "utf-8" )
	return model.similarity(u1, u2)

def all_similarity(word,model):
	variable = globals()[model]
	variable.seek(0) 
	lines = variable.read().splitlines()
	for line in lines:
			turkish = line.split(":")[0]
			
			try:
				result = similarity_compare(word,turkish)
				similarity_index[turkish] = result 
			except:
				pass

	print "word: ", word			
	for k, v in sorted(similarity_index.items(), key=itemgetter(1), reverse=True):
		print k, v
	print "randomly selected most similar"
	print choice(Counter(similarity_index).most_common(2))[0]
					
	

all_similarity("adam","verb")					
#similarity_compare("ağaç","çiçek")
def valid_finder(word):
	u1 = unicode( word, "utf-8" )
	return model[u1]


#print valid_finder("güzel")	


