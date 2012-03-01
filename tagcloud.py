import operator
from pprint import pprint
from functions import *
from wordcomplete import wcomp
   
"""
Creates a tag cloud for the given article

Returns code for a wordle applet
Applet from http://www.wordle.com
"""
def make_cloud(docid, searcher, term_freq, cont):
  sorted_words = get_keywords(docid, searcher, term_freq)
  
  print cont
  
  output = '<div id="ac">\
    <applet \
      name="wordle"\
      mayscript="mayscript"\
      code="wordle.WordleApplet.class"\
      codebase="http://wordle.appspot.com"\
      archive="/j/v1356/wordle.jar" \
      width="800" height="600">\
      <param name="wordcounts" value="'

  for i in range(0,10):
    print sorted_words[i][0]
    output += wcomp(sorted_words[i][0],cont) +':'+ str(sorted_words[i][1]) + ',' 
    
  output += '"/>\
      <param name="java_arguments" value="-Xmx256m -Xms64m">\
      Your browser doesn\'t seem to understand the APPLET tag.\
      You need to install and enable the <a href="http://java.com/">Java</a> plugin.\
    </applet>\
  </div>'
  return output