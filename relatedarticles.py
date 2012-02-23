import functions

def find_related(docid, searcher):
  keywords = functions.get_keywords(docid, searcher)
  query = ""
  for word in keywords[:5]:
    query = query + word[0] + " "
  print "query:"
  print query
  res = searcher.find("content", unicode(query), limit=3)
  
  print 'related articles'
  for r in res:
    print r['title']
  return res