import operator
from pprint import pprint
from functions import *
from wordcomplete import wcomp
   
"""
Creates a tag cloud for the given article

Returns code for a wordle applet
Applet from http://www.wordle.com
"""
def make_cloud(docid, searcher, term_freq, cont, tf=None):
  sorted_words = get_keywords(docid, searcher, term_freq, tf)
  
  output = ''
  for i in range(0,10):
    output += wcomp(sorted_words[i][0],cont) +':'+ str(sorted_words[i][1]) + ',' 
    
  return output