import operator
from pprint import pprint
def print_cloud(words):
  for w in words:
    print w
    
def make_cloud(words):
  sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1))
  
  sorted_words.reverse()
  output = '<form action="http://www.wordle.net/advanced" method="POST"> <textarea name="wordcounts" style="display:none">'

  for i in range(0,10):
    output += sorted_words[i][0] +':'+ str(sorted_words[i][1])
    
  output += '</textarea> <input type="submit" value="Woordenwolk"> </form>'
  return output
