from collections import defaultdict
import codecs

class LocationFinder:
  
  """
  On initialization: Read the location database from the given text file
  and store it in memory in a dictionary for fast lookup.
  """
  def __init__(self, filename):
    f = codecs.open(filename, 'r', encoding='utf-8')

    location_data = defaultdict(list)

    temp_data = []
    for l in f.readlines():
      
      # Some entries are split into multiple lines in the file.
      # Save the first half and prepend that to the next line to s
      # process the entry as a whole.
      if temp_data:
	d = temp_data + l.split("\t")[1:]
      else:
	d = l.split("\t")
      if (len(d) < 10):
        temp_data = d
        continue
      else:
        temp_data = []
      
      #Extract all possible names of a location
      names = [d[1]]
      if d[2]:
	names.extend(d[2].split(","))
	
      #Append data to dictionary under all possible names
      for n in names:
	location_data[n.lower().strip()].append({'id': d[0], 'name': d[1], 'type': d[4], 'pop': int(d[5]), 'lat': d[6], 'lon': d[7], 'country': d[8]})
    self.location_data = location_data

  """
  Attempt to find a place given is name
  Return a dict with relevant data
  (name, location, population, type, etc)
  """
  def find(self, place):
    possible_places = self.location_data[place.lower()]
    
    if len(possible_places) == 0:
      return None
    
    largest_place = {'pop': 0}
    for p in possible_places:
      
      if p['type'] == 'country':
	return p
      elif p['pop'] > largest_place['pop']:
        largest_place = p
    return largest_place
  
  """
  Create a link to a google map image given a set of locations
  """
  def create_google_map(self, places):
    locstring = ''
    displayed_locs = []
    #Create link for all locations
    for p in places:
      displayed_locs.append(p['name'])
      locstring += '&markers=%7Ccolor:red%7Clabel:' + p['name'][0] + '%7C'
      if p['lat'] and p['lon']:
        latitude = p['lat'][0:-2] + "." + p['lat'][-2:]
        longitude = p['lon'][0:-2] + "." + p['lon'][-2:]
        locstring += latitude + "," + longitude
        
      #As a fallback, send the location name to Google if you do not have coordinates
      else:
        locstring += p['name']
      
    return (displayed_locs, "http://maps.googleapis.com/maps/api/staticmap?size=400x400" + locstring + "&zoom=3&sensor=false")
    
  """
  Given a piece of text, try to find any locations within that text,
  and return a link to a google map image with those locations marked
  """
  def find_locs_in_text(self, text, reader):
    location_hints = ['in', 'of', 'to', 'from', 'at']
    mark = False
    found_locations = []
    
    for word in text.split(" "):
      if mark and word.istitle():
	#skip common words
	freq_cont = reader.doc_frequency("content", word.lower())
	if freq_cont < 2000:
	  place = self.find(word)
	  if place and place not in found_locations:
	    found_locations.append(place)
      mark = False
      
      if word in location_hints:
	mark = True
    return self.create_google_map(found_locations)