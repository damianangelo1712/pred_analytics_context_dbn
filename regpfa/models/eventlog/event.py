class Event:
    def __init__(self,id, name, timestamp, further_attributes):
        self.id = id
        self.name = name
        self.timestamp = timestamp
        self.further_attributes = further_attributes

    def __repr__(self):
        return '{}'.format(self.name)

    def getTimestamp(self):
        return self.timestamp
