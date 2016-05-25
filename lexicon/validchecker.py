# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pdb


model = Word2Vec.load_word2vec_format('trcorpus.bin', binary=True)
def valid_finder(fn):

	
	with open(fn+".txt","r") as words:
		lines = words.read().splitlines()
		for word in lines:	
			u1 = unicode( word, "utf-8" )
			try:
				model[u1]
				with open(fn +".new" , "a") as output:

					output.write(u1 + "\n")
				print "success: ",u1

			except:
				print "failed: ",u1
				continue


valid_finder("gender")				
