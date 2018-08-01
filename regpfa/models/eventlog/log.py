import collections
import operator


class Log:
    def __init__(self):
        self.traces = []
        self.symbolmapping = []
        self.nocontextelements = 0
    def append(self, trace):
        self.traces.append(trace)
        self.set_symbolmapping()

    def get_numberofsymbols(self):
        return sum(map(lambda x: x.get_numberofsymbols(), self.traces))

    def get_alleventsByName(self):
        all_events = []
        for trace in self.traces:
            for event in trace.events:
                all_events.append(event.name)
        return all_events

    def get_alleventsByID(self):
        all_events = []
        for trace in self.traces:
            for event in trace.events:
                all_events.append(self.get_symbolidfromname(event.name))
        return all_events

    def get_allstartevents(self):
        all_events = []
        for trace in self.traces:
            all_events.append(self.get_symbolidfromname(trace.get_firsteventfrompath()))
        return all_events

    def get_allendevents(self):
        all_events = []
        for trace in self.traces:
            all_events.append(self.get_symbolidfromname(trace.get_lasteventfrompath()))
        return all_events

    def get_uniqueSymbolsByName(self):
        return self.get_symbolmapping().values()

    def get_uniqueSymbolsByID(self):
        return self.get_symbolmapping().keys()

    def get_numberOfUniqueSymbols(self):
        return len(self.get_uniqueSymbolsByName())

    def get_symbolfrequency(self):
        return collections.Counter(self.get_alleventsByName())

    def get_startsymbolfrequency(self):
        all_symbols = self.get_symbolmapping()
        existing_start_symbols = collections.Counter(self.get_allstartevents())
        for key, value in all_symbols.items():
            all_symbols[key] = existing_start_symbols[key]
        return all_symbols

    def get_endsymbolfrequency(self):
        all_symbols = self.get_symbolmapping()
        existing_start_symbols = collections.Counter(self.get_allendevents())
        for key, value in all_symbols.items():
            all_symbols[key] = existing_start_symbols[key]
        return all_symbols

    ## Replace/Map Activity names by numeric IDs
    def set_symbolmapping(self):
        unique_events = set(self.get_alleventsByName())
        if not self.symbolmapping:
            unique_ids = range(0, len(unique_events))
            self.symbolmapping = dict(zip(unique_ids, unique_events))
        else:  # only add events not already in the mapping to keep IDs stable
            curr_mapping = self.get_symbolmapping()
            curr_events = set(curr_mapping.values())
            diff = unique_events.difference(curr_events)
            max_key = max(curr_mapping.keys())
            unique_ids = range(max_key + 1, len(unique_events))
            new_mapping = dict(zip(unique_ids, diff))
            self.symbolmapping = {**new_mapping, **curr_mapping}

    def get_symbolmapping(self):
        return self.symbolmapping

    def get_symbolnamefromid(self, id):
        symbolmapping = self.get_symbolmapping()
        return symbolmapping[id]

    def get_symbolidfromname(self, name):
        symbolmapping = dict(self.get_symbolmapping())
        inv_mapping = {v: k for k, v in symbolmapping.items()}
        return inv_mapping[name]
    def setcontextelemts(self, nocontextelements):
        self.nocontextelements = nocontextelements