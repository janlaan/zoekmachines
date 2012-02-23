import functions

def format_related_articles(res):
  if(len(res) == 0):
    return '<p>No related articles found'
  else:
    out = '<ul>'
    for r in res:
      out += '<li><a href="display?docid='+ r['id'] +'">'+ r['title'] +'</a></li>'
    out += '</ul>'
    return out

def find_related(docid, searcher, num_keywords=3):
  keywords = functions.get_keywords(docid, searcher)
  query = ""
  for word in keywords[:num_keywords]:
    query = query + word[0] + " "
  print "query:"
  print query
  res = searcher.find("content", unicode(query), limit=3)
  if(len(res) <= 1 and num_keywords > 1):
    return find_related(docid, searcher, num_keywords - 1)
  print 'related articles'
  for r in res:
    print r
  return format_related_articles(res)