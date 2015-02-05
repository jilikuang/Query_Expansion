import sys
import search_engine
import xml_parser
import Document

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
    result = se.search(query)

    entries = xml_parser.parse_entries(result)

    print 'Total no of results: ' + str(len(entries))
    if len(entries) < 10:
        print 'Abort due to fewer than 10 results'
        return

    # User judgement and generate list for algo
    docs = []

    print 'Bing search results:'
    print '======================'

    for i in range(len(entries)):
        url = entries[i].get_url()
        title = entries[i].get_title()
        desc = entries[i].get_description()
        print 'Result ' + str(i+1)
        print '['
        print ' URL: ' + url
        print ' Title: ' + title
        print ' Summary: ' + desc
        print ']'
        relevance = True
        judge = raw_input('Relevant (Y/N)? ')
        if judge == 'N' or judge == 'n':
            relevance = False
        docs.append(Document.Document(title, url, desc, relevance))

if __name__ == "__main__":
    main(sys.argv[1:])
