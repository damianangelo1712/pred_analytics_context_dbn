from .event import Event

class Trace:
    def __init__(self, name):
        self.name = name
        self.events = []
        self.predicted_next_event = None

    def __repr__(self):
        return '{}: {}'.format(self.name, self.get_path())

    def append(self, event):
        self.events.append(event)

    def get_path(self):
        path = sorted(self.events, key=Event.getTimestamp)
        path_names = []
        for event in path:
            path_names.append(event.name)
        return path_names

    def get_pathwithoutlastevent(self):
        path = sorted(self.events, key=Event.getTimestamp)
        path_names = []
        for event in path[:-1]:
            path_names.append(event.name)
        return path_names

    def get_pathlength(self):
        return len(self.get_path())

    def get_numberofsymbols(self):
        return len(self.events)

    def get_firsteventfrompath(self):
        path = self.get_path()
        return path[0]

    def get_lasteventfrompath(self):
        path = self.get_path()
        return path[-1]
