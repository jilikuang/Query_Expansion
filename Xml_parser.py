import re
import xml.etree.ElementTree as etree

def parse_entries(xml_obj):
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
