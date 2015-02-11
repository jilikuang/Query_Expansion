import urllib2
import base64

def get_engine(key):
    """
    get_engine(<Bing Key>)
    Get the search engine object of the Bing key
    """
    return SearchEngine(key)

def format_query(query, option=''):
    """
    format_query(<list of query>[, option={'url', 'file'}])
    Format a query string formed from the query list
    Option 'url' will use '%20' for the space and enclose the string with '%27'
    Option 'file' will use '_' to replace the space
    """
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
        """ A search engine object possesses its own Bing key """
        self.key = key

    def get_key(self):
        """
        get_key()
        Get the Bing key which the search engine is using
        """
        return self.key

    def set_key(self, key):
        """
        set_key(<Bing Key>)
        Set the new Bing key to the search engine
        """
        self.key = key

    # pass query to Bing search API and return the results
    def search(self, query, test=None):
        """
        search(<query list>[, test=<input xml file>])
        Use Bing to search for results with a query list
        test can be assigned with a previous result XML file for testing
        A XML object will be returned as result
        """
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
            # If test file is provided, use the saved result for testing
            print '[Test] Open XML file ' + test
            response = open(test, 'r')
        else:
            response = urllib2.urlopen(req)
        # response is readable (read method is implemented),
        # it may be passed out directly to XML Element Tree parser
        return response
