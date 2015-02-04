import urllib2
import base64

class SearchEngine:

    accountKey = '6SBqV1l4XaDnfx+w4rPVqyEgtNJqvUJu50wXdg5njhk'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}

    @staticmethod
    def getResult(terms):
        f = open('result', 'r')
        return f.read()             #don't use API too often

        bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?' + terms
        req = urllib2.Request(bingUrl, headers = SearchEngine.headers)
        response = urllib2.urlopen(req)
        content = response.read()
        # content contains the xml/json response from Bing.
        return content


