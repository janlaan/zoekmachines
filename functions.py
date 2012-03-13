from load import get_term_freq_doc
import operator
import re

"""
Returns the keywords from any given article,
ordered by relevance according to TF / IDF score
"""
def get_keywords(docid, searcher, term_freq):
  idf = term_freq
  tf = get_term_freq_doc(docid, searcher)
  scores = calc_idf_score(idf, tf)
  sorted_scores = sorted(scores.iteritems(), key=operator.itemgetter(1))
  sorted_scores.reverse()
  
  sorted_scores2 = []
  
  for i in range(len(sorted_scores)):
    if not re.search("[0-9]", sorted_scores[i][0]):
      sorted_scores2.append(sorted_scores[i])
      
  return sorted_scores2
  
"""
Calculates the TF / IDF score for the given text
"""
def calc_idf_score(idf, tf):
  res = {}
  for t in tf:
    if idf[t] < 20:
      res[t] = 1
    else:
      res[t] = tf[t] * (10000 / idf[t])
  return res