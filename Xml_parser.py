import re
import xml.etree.ElementTree as etree

def parse_entries(xml_obj):
    """
    parse_entries(<xml object>)
    Parse the XML object to retrieve each result entry
    Return a list of self-defined QueryEntry objects of entry
    """
    tree = etree.parse(xml_obj)
    root = tree.getroot()
    entries = []
    for child in root:
        match = re.search('.*entry$', child.tag)
        if match != None:
            entries.append(QueryEntry(child))
    return entries

class QueryEntry:

    def __init__(self, entry):
        """
        QueryEntry(<xml entry>)
        Parse the content of the XML entry to form a QueryEntry object
        A QueryEntry object contains the title, URL, and the description
        """
        self.entry = entry
        self.content = None
        for child in self.entry:
            match = re.search('.*content$', child.tag)
            if match != None:
                self.content = child
                break
        self.title = None
        self.description = None
        self.url = None
        if self.content != None:
            if len(self.content) > 0:
                for child in self.content[0]:
                    match = re.search('.*Title$', child.tag)
                    if match != None:
                        self.title = child.text
                        continue
                    match = re.search('.*Description$', child.tag)
                    if match != None:
                        self.description = child.text
                        continue
                    match = re.search('.*Url', child.tag)
                    if match != None:
                        self.url = child.text

    def get_title(self):
        """
        get_title()
        Get the title of the entry
        """
        return self.title

    def get_description(self):
        """
        get_description()
        Get the description of the entry
        """
        return self.description

    def get_url(self):
        """
        get_url()
        Get the URL of the entry
        """
        return self.url
