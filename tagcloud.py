import operator
from pprint import pprint
def print_cloud(words):
  for w in words:
    print w
    
def make_cloud(words):
  sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1))
  
  sorted_words.reverse()
  output = ''
  for i in range(0,10):
    output += '<span style="font-size: ' + str(sorted_words[i][1]) +'em;">' + sorted_words[i][0] + "</span>  &nbsp;&nbsp; "
  
  return output