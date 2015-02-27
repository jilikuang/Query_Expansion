import sys
import Search_engine
import Xml_parser
import Document
import QueryExpansion

def save_xml(xml_obj, query=None):
    """
    save_xml(<XML object>[, query=<query list>])
    Save the the XML object to a XML file and return the file name string
    The query list can be optionally provided to form the postfix of the file
    """
    qfix = ''
    if query != None:
        qfix = '_' + Search_engine.format_query(query, 'file')
    output = 'result' + qfix + '.xml'
    f = open(output, 'w')
    f.write(xml_obj.read())
    f.close()
    return output

def main(argv):
    """
    main(argv)
    The entry point of the application
    """
    if len(argv) == 3:
        if argv[0] == 'test':
            # Use the default Bing key
            bing_key = '6SBqV1l4XaDnfx+w4rPVqyEgtNJqvUJu50wXdg5njhk'
            target = float(argv[1])
            query = argv[2:]
        else:
            bing_key = argv[0]
            target = float(argv[1])
            query = argv[2:]
    else:
        print 'Usage: <key> <target> <query>'
        return

    # Initalization for routine
    se = Search_engine.get_engine(bing_key)
    routine_cnt = 0
    precision = 0

    # Start of searching process (to loop)
    while precision < target:
        routine_cnt += 1
        print 'Parameters:'
        print 'Client key = ' + bing_key
        print 'Query      = ' + Search_engine.format_query(query)
        print 'Precision  = ' + str(target)

        result = se.search(query)

        # Save each result under testing
        if argv[0] == 'test':
            xml_file = save_xml(result, query)
            result = open(xml_file, 'r')

        # Retrieve the entry list from the result XML object
        entries = Xml_parser.parse_entries(result)

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
            print ' Title: ' + title.encode('ascii', 'ignore')
            print ' Summary: ' + desc.encode('ascii', 'ignore')
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
        print 'Query ' + Search_engine.format_query(query)
        print 'Precision ' + str(precision)
        if precision >= target:
            print 'Desired precision reached, done'
            break
        if precision == 0.0:
            print 'No relevant result'
            break

        # Apply algo
        print 'Still below the desired precision of ' + str(target)
        print 'Indexing results ....'
        calculator = QueryExpansion.QueryExpansion(query)
        query = calculator.get_new_query(docs, query)

if __name__ == "__main__":
    main(sys.argv[1:])
