import urllib2
import base64

def get_engine(key):
    return SearchEngine(key)

def format_query(query, option=''):
    if option == 'url':
        sep = '%20'
    elif option == 'file':
        sep = '_'
    else:
        sep = ' '
    q = sep.join(query)
    if option == 'url':
        q = '%27' + q + '%27'
    return q

class SearchEngine:

    def __init__(self, key=None):
        self.key = key

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    # pass query to Bing search API and return the results
    def search(self, query, test=None):
        if self.key == None:
            print 'Error: There is no key'
            return None
        # Form the overall query URL
        bing_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query='
        search_option = '&$top=10&$format=Atom'
        query = format_query(query, 'url')
        url = bing_url + query + search_option

        # Form the header with Bing key for search
        key_enc = base64.b64encode(self.key + ':' + self.key)
        headers = {'Authorization': 'Basic ' + key_enc}

        # Instantiate the request and issue it
        print 'URL: ' + url
        req = urllib2.Request(url, headers=headers)
        if test != None:
            # [Develop] Use saved result for test
            print '[Test] Open XML file ' + test
            response = open(test, 'r')
        else:
            response = urllib2.urlopen(req)
        # response is readable (read method is implemented),
        # it may be passed out directly to XML Element Tree parser
        #content = response.read()
        # content contains the xml/json response from Bing.
        return response
