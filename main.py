import sys
import search_engine
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
    print 'Query      = ' + search_engine.format_query(query)
    print 'Precision  = ' + str(precision)

    se = search_engine.get_engine(bing_key)
    result_xml = se.search(query)

if __name__ == "__main__":
    main(sys.argv[1:])
