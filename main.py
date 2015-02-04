import sys
import SearchEngine
import xml.dom.minidom

def main(argv):
    #for arg in argv: print arg
    if len(argv) < 2:
        print 'Too few arguments'
        return
    if len(argv) < 3:
        bing_key = 'default Bing Account Key'
        precision = float(argv[0])
        query = argv[1:]
    else:
        bing_key = argv[0]
        precision = float(argv[1])
        query = argv[2:]

    print 'Bing Account Key: ' + bing_key
    print 'Precision: ' + str(precision)
    print 'Query: ' + str(query)

    #query = 'Query=%27gates%27&$top=10&$format=Atom'
    #res = SearchEngine.SearchEngine.getResult(query)
    #print res

if __name__ == "__main__":
    main(sys.argv[1:])
