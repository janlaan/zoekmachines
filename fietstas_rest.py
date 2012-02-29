#!/usr/bin/env python 
"""Fietstas REST API library.

Author: Valentin Jijkoun <jijkoun at uva dot nl> 

(c) 2009-2010 ISLA, University of Amsterdam
"""

import sys
import urllib, urllib2
import time


DEFAULT_FIETSTAS_LOCATION = "http://fietstas.science.uva.nl:8080"

class FietstasError(Exception):
    pass

class Fietstas(object):
    """Fietstas API provider"""

    def __init__(self, url=DEFAULT_FIETSTAS_LOCATION, key=None):
        """Initialize a Fietstas API provider instance. 
          - url: location of the Fietstas REST services
          - key: Fietstas API key (required)
        """  

        ## Location of Fietstas service
        self.base_url = url

        ## API key
        self.key = key

    def upload_document(self, **params):
        """Upload a document to Fietstas.

        As parameters this method takes document parameters (see http://fietstas.science.uva.nl/rest-reference.php)
        """

        assert 'document' in params and isinstance(params['document'], basestring)
       
        # Add key parameter, unless it specified explicitly 
        if 'key' not in params:
            params['key'] = self.key

        # Make sure all parameters are strings or integers
        for name, val in params.items():
            assert isinstance(val, (int, basestring)), "Illegal value for parameter '%s': expected string or int, got %s" % (name, type(val))
            # Encode unicode values 
            if isinstance(val, unicode):
                params[name] = val.encode("utf-8") 

        # Make POST request 
        code, headers, text = self.post_request(self.base_url + '/doc', params)
        
        # The id of the uploaded doc should be in the header
        if 'X-Fietstas-Document-Id' in headers:
            return headers['X-Fietstas-Document-Id']
        
        return None    

    def get_document_info(self, id=None, tags=None):
        """List information for documents specified either by id or by any of the tags.

         - id: id of the document
         - tags: string with comma-separated list of document tags

         Either id or tags should be specified, but not both.
        """

        params = {'key': self.key}
        if id is not None:
            params['id'] = id
        elif tags is not None:
           params['tags'] = tags
        else:
            raise ValueError("Either id or tags should be specified")

        # Make GET request 
        code, headers, text = self.get_request(self.base_url + '/doc', params)

        if code >= 200 and code < 300:
            return text

        return None    

    def make_cloud(self, **params):
        """Make a term cloud with given parameters
          - params: document parameters (see http://fietstas.science.uva.nl/rest-reference.php)

          Returns a pair (permalink, content) where 'permalink' is URL of the request result (can
          also be passed to Fietstas.get_cloud()) and 'content' is the content of the cloud (or
          None if not available yet). 

          If an error occurs, permalink is None and content is the error message from Fietstas.
        """

        assert 'docs' in params or 'tags' in params
       
        # Add key parameter, unless it specified explicitly 
        if 'key' not in params:
            params['key'] = self.key
       
        # Make sure all parameters are strings or integers
        for name, val in params.items():
            assert isinstance(val, (int, basestring)), "Illegal value for parameter '%s': expected string or int, got %s" % (name, type(val))
            # Encode unicode values 
            if isinstance(val, unicode):
                params[name] = val.encode("utf-8") 

        # Make POST request 
        code, headers, text = self.post_request(self.base_url + '/cloud', params)
      
        return self._extract_cloud(code, headers, text) 

    def get_cloud(self, permalink):
        """Fetch the cloud with a given permalink (e.g., returned by make_cloud()).
        
        Returns cloud content or None if it is not available. 
        """
        
        # Make GET request 
        code, headers, text = self.get_request(permalink)

        _, content = self._extract_cloud(code, headers, text) 

        return content

    def _extract_cloud(self, code, headers, text):
        """Extract cloud based on HTTP response code, headers and message"""    

        if code >= 300:
            return None, text
        
        # Take permalink, status and message from the headers
        permalink = headers.get('X-Fietstas-Request-Permalink');
        status = headers.get('X-Fietstas-Request-Status');
        message = headers.get('X-Fietstas-Request-Message');

        if permalink is None or status == 'error':
            return None, message

        if status in ['completed', 'partial']:
            return permalink, text
        
        return permalink, None

    def post_request(self, url, params):
        """Make a POST request to the given url, with params as request data"""

        # Encode parameters as request data
        data = urllib.urlencode(params)

        # Build the request
        req = urllib2.Request(url, data)

        # Execute it
        return self._make_request(req)

    def get_request(self, url, params={}):
        """Make a GET request to the given url with params"""

        # Encode parameters as query part of the URL
        if params:
            query_part = '?' + urllib.urlencode(params)
        else:
            query_part = ''

        # Build the request
        req = urllib2.Request(url + query_part)

        # Execute it
        return self._make_request(req)

    def _make_request(self, req):
        """Perform a HTTP request req. Returns a tuple of (response_code, response_headers, response_text)"""

        try:
            # Open the url
            response = urllib2.urlopen(req)
            code = response.code
            headers = response.info()
            # Read the response
            text = response.read()
        except urllib2.HTTPError, e:
            code = e.code
            headers = e.headers
            text = e.read()
            if code >= 300:
                raise FietstasError(text)

        # Return the result
        return code, headers, text

  
def main():

    # The code below demonstrates how to use the library

    f = Fietstas(key='demo-key')

    doc_id = f.upload_document(document="blah blah blah", tags="spam")
    print "Uploaded doc %s" % doc_id

    doc_info = f.get_document_info(id=doc_id)
    print "Document info:"
    print doc_info

    doc_info = f.get_document_info(tags='spam')
    print "Document with tags 'spam':"
    print doc_info

    cloud_link, cloud = f.make_cloud(docs=doc_id, words=1)
    print "Generated cloud: %s" % cloud_link

    if cloud is None:
        # Cloud is not available yet: wait in a loop
        for i in range(10):
            time.sleep(2)
            print "Attempt %d" % (i + 1)
            cloud = f.get_cloud(cloud_link)
            if cloud is not None:
                break
    print "Cloud content: "
    print cloud

if __name__ == "__main__":
    sys.exit(main())

