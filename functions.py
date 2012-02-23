from load import get_term_freq_col, get_term_freq_doc
import operator
from pprint import pprint

def get_keywords(docid, searcher):
  idf = get_term_freq_col()
  tf = get_term_freq_doc(docid, searcher)
  
  scores = calc_idf_score(idf, tf)
  sorted_scores = sorted(scores.iteritems(), key=operator.itemgetter(1))
  sorted_scores.reverse()
  pprint(sorted_scores[:10])
  return sorted_scores
  

def calc_idf_score(idf, tf):
  res = {}
  for t in tf:
    if idf[t] < 20:
      res[t] = 1
    else:
      res[t] = tf[t] * (10000 / idf[t])
  return res