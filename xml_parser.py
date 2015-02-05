import re
import xml.etree.ElementTree as etree

def get_parser(xml_obj):
    return XMLParser(xml_obj)

class QueryEntry:

    def __init__(self, entry):
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
        return self.title

    def get_description(self):
        return self.description

    def get_url(self):
        return self.url

class XMLParser:

    def __init__(self, xml):
        self.et = etree.parse(xml)
        self.root = self.et.getroot()
        self.entries = []
        for child in self.root:
            match = re.search('.*entry$', child.tag)
            if match != None:
                self.entries.append(child)

    def get_entry_num(self):
        return len(self.entries)

    def parse_entry(self, index):
        if index >= len(self.entries):
            print 'Invalid entry index'
            return None
        entry = QueryEntry(self.entries[index])
        return entry
