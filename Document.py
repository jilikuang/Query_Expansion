class Document:

    def __init__(self, title, url, des, relevant):
        self.title = title                  # string
        self.url = url                      # string
        self.description = des              # string
        self.is_relevant = relevant         # True or False
