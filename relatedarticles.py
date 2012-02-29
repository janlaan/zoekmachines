import functions

def format_related_articles(res, docid):
  if(len(res) == 0):
    return '<p>No related articles found'
  else:
    out = '<br /><h3>Related articles:</h3>\
    <ul>'
    for r in res:
      if r['id'] != docid: #remove the article iteself from the result set
        out += '<li><a href="display?docid='+ r['id'] +'">'+ r['title'] +'</a></li>'
    out += '</ul>'
    return out

"""
Find (at most 3) related articles for the article with the given docid

Returns links to the articles in an unordened list
"""
def find_related(docid, searcher, term_freq, num_keywords=3):
  #Combine the most relevant keywords into one search query
  keywords = functions.get_keywords(docid, searcher, term_freq)
  query = ""
  for word in keywords[:num_keywords]:
    query = query + word[0] + " "
  
  #Try to find related articles
  res = searcher.find("content", unicode(query), limit=4)
  
  
  #If no related articles were found, try again with one less keyword
  if(len(res) <= 1 and num_keywords > 1):
    return find_related(docid, searcher, term_freq, num_keywords - 1)
    
  return res #format_related_articles(res, docid)