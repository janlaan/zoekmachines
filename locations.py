from collections import defaultdict

class LocationFinder:
  def __init__(self, filename):
    f = open(filename, 'r')

    location_data = defaultdict(list)

    temp_data = []
    for l in f.readlines():
      d = temp_data + l.split("\t")
      if (len(d) < 10):
        temp_data = d
        continue
      else:
        temp_data = []
      location_data[d[1]].append({'id': d[0], 'pop': d[5], 'lat': d[6], 'lon': d[7]})
    self.location_data = location_data

  def find_place(self, place):
    possible_places = self.location_data[place]
    
    if len(possible_places) == 0:
      return None
    
    largest_place = {'pop': 0}
    for p in possible_places:
      if p['pop'] > largest_place['pop']:
        largest_place = p
    return largest_place
    
  def create_google_map(self, place):
    latitude = place['lat'][0:-2] + "." + place['lat'][-2:]
    longitude = place['lon'][0:-2] + "." + place['lon'][-2:]
    locstring = latitude + "," + longitude
    return "http://maps.googleapis.com/maps/api/staticmap?size=400x400&center=" + locstring + "&markers=%7Ccolor:red%7C" + locstring + "&zoom=3&sensor=false"