import sys
import search_engine
import xml_parser
import Document

def save_xml(xml_obj, query=None):
    qfix = ''
    if query != None:
        qfix = '_' + search_engine.format_query(query, 'file')
    output = 'result' + qfix + '.xml'
    f = open(output, 'w')
    f.write(xml_obj.read())
    f.close()
    return output

def main(argv):
    #for arg in argv: print arg
    if len(argv) < 2:
        print 'Too few arguments'
        return
    if len(argv) > 2 and argv[0].startswith('--key='):
        bing_key = argv[0][6:]
        target = float(argv[1])
        query = argv[2:]
    else:
        # Use the default Bing key
        bing_key = '6SBqV1l4XaDnfx+w4rPVqyEgtNJqvUJu50wXdg5njhk'
        target = float(argv[0])
        query = argv[1:]

    # Initalization for routine
    se = search_engine.get_engine(bing_key)
    routine_cnt = 0
    precision = 0

    # Start of searching process (to loop)
    while precision < target:
        routine_cnt += 1
        print 'Parameters:'
        print 'Client key = ' + bing_key
        print 'Query      = ' + search_engine.format_query(query)
        print 'Precision  = ' + str(target)

        result = se.search(query, test='result.xml')

        if True:
            xml_file = save_xml(result, query)
            print 'Resuls is saved as ' + xml_file
            result = open(xml_file, 'r')

        entries = xml_parser.parse_entries(result)

        print 'Total no of results: ' + str(len(entries))
        if len(entries) < 10:
            print 'Abort due to fewer than 10 results'
            break

        # User judgement and generate list for algo
        docs = []
        accept_cnt = 0.0
        print 'Bing Search Results:'
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
            else:
                accept_cnt += 1
            docs.append(Document.Document(title, url, desc, relevance))

        # Check precision
        print str(accept_cnt) + ' ' + str(len(entries))
        precision = accept_cnt / len(entries)
        print '======================'
        print 'Feedback Summary'
        print 'Query ' + search_engine.format_query(query)
        print 'Precision ' + str(precision)
        if precision >= target:
            print 'Desired precision reached, done'
            break

        # Apply algo
        print 'Still below the desired precision of ' + str(target)

if __name__ == "__main__":
    main(sys.argv[1:])
