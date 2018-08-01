import re
import opyenxes.data_in.XesXmlParser as xes_parse
from regpfa.models.eventlog.log import Log
from regpfa.models.eventlog.trace import Trace
from regpfa.models.eventlog.event import Event


def parsexes(file):
    """
    Reads xes file and transforms to RegPFA Log object
    """
    # Create new xes parser
    xes_file = xes_parse.XesXmlParser()

    # Parse xes input file to xes log element
    xes_log = xes_file.parse(file)

    # Transform xes log to RegPFA log

    eventlog = Log()

    # Extract XLog
    xlog = xes_log[0]


    for trace_element in xlog:
        trace = Trace(trace_element.get_attributes()['concept:name']) #naive approach, I think it is not always 'concept:name'
        i = 0
        attr_counter = 0
        for event_element in trace_element:
            if str(event_element.get_attributes()['lifecycle:transition']) == 'complete':
                i += 1
                event_name = str(event_element.get_attributes()['concept:name']) #naive approach, I think it is not always 'concept:name'
                event_timestamp = event_element.get_attributes()['time:timestamp'].get_value() #naive approach, I think it is not always 'concept:name'
                event_attr = event_element.get_attributes()
                del event_attr['concept:name']
                del event_attr['time:timestamp']
                event_attr_dict = {}

                for key, value in event_attr.items():
                    event_attr_dict[key] = value.get_value()
                event = Event(i, event_name, event_timestamp, event_attr_dict)
                attr_counter= len(event_attr_dict.keys())-1
                print(event)
                trace.append(event)
        eventlog.setcontextelemts(attr_counter)
        eventlog.append(trace)

    return eventlog

#def parsecsv(file):
    #TODO

#def parsecelonis(pythonapi):
    #TODO

#def parserapidminer(something):
    #TODO