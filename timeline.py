from pprint import pprint
from collections import defaultdict
from whoosh import query

class Timeline:

  """
  Initialize the timeline: calculate the __relative__ frequency per day
  for the given words
  """
  def __init__(self, words, application):
    self.overall_frequency = defaultdict(float)
    self.frequencies = defaultdict(list)
    self.frequencies_avg = defaultdict(list)
    
    for w in words:
      #Calculate overall average frequency
      self.overall_frequency[w] = application.reader.doc_frequency("content", w) / 30.0
      
      #Calculate frequency for each day
      if self.overall_frequency[w] > 0:
        content_f = application.searcher_frequency.find("content", w, limit=9999)
        for i in range(1, 31):
          datefilter = query.Term("pubdate", unicode("200704{0:02d}T000000".format(i)))
          res = application.searcher_frequency.find("content", w, limit=9999, filter=datefilter)
          self.frequencies[w].append(len(res))
          self.frequencies_avg[w].append(len(res) / self.overall_frequency[w])
  """
  Retrieve calculated data
  """
  def get_data(self):
    return self.frequencies_avg