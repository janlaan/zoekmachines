import operator
from pprint import pprint
from functions import *
from math import log10
    
def make_cloud(docid, searcher):
  sorted_words = get_keywords(docid, searcher)
  
  output = '<form action="http://www.wordle.net/advanced" method="POST"> <textarea name="wordcounts" style="display:none">'

  for i in range(0,10):
    output += sorted_words[i][0] +':'+ str(log10(sorted_words[i][1])) + '\n' 
    
  output += '</textarea> <input type="submit" value="Woordenwolk"> </form>'
  return output
