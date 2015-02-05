import sys
import SearchEngine
import xml.dom.minidom

def main(argv):
    #for arg in argv: print arg
    if len(argv) < 2:
        print 'Too few arguments'
        return
    if len(argv) > 2 and argv[0].startswith('--key='):
        bing_key = argv[0][6:]
        precision = float(argv[1])
        query = argv[2:]
    else:
        # Use the default Bing key
        bing_key = '6SBqV1l4XaDnfx+w4rPVqyEgtNJqvUJu50wXdg5njhk'
        precision = float(argv[0])
        query = argv[1:]

    # Start of searching process (to loop)
    print 'Parameters:'
    print 'Client key = ' + bing_key
    print 'Query      = ' + str(query)
    print 'Precision  = ' + str(precision)

    #query = 'Query=%27gates%27&$top=10&$format=Atom'
    #res = SearchEngine.SearchEngine.getResult(query)
    #print res

if __name__ == "__main__":
    main(sys.argv[1:])
