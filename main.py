import SearchEngine
import xml.dom.minidom

def main():
    query = 'Query=%27gates%27&$top=10&$format=Atom'
    res = SearchEngine.SearchEngine.getResult(query)
    print res

main()
