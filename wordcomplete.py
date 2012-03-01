def searchwords(stam,lijst):
  newList = []

  for word in lijst:
    if word.lower().startswith(stam):
      newList.append(word)

  return newList

def wcomp(stam,words):
  list = words.split()
  punctuation = [',','(',')',':',';','<','>','"','?','/','!']
  list = [''.join(c for c in s if c not in punctuation) for s in list]
  newList = searchwords(stam,list)

  if not newList:
    newList = searchwords(stam[:-1:],list)

  if not newList:
    return stam
  else:
    return min(newList, key = len)