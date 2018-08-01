import re
from regpfa.models.eventlog import *

counter = 0

def eventMaker(event_string):
    '''
    input: a list of strings denoting an event read from xes file
              eg:- ['\t\t<event>\n',
              '\t\t\t<string key="concept:instance" value="3885"/>\n',
              '\t\t\t<int key="Qty for MRB" value="0"/>\n',
               '\t\t\t<string key="lifecycle:transition" value="complete"/>\n', '\t\t</event>\n']

    output: an object of Event class made from the input string
    '''

    # removing <event> and <\event> from the list
    del event_string[0]
    del event_string[-1]

    # making a key value pair (i.e dictionary) of all the lines in the list
    event_dict = dict()
    for i in event_string:
        pattern = re.compile(r'(".*").*(".*")')
        found = [m.replace('"', '') for m in pattern.findall(i)[0]]
        if found:
            event_dict[found[0]] = found[1]

    # using the event dict to make an Event object
    global counter
    id = counter
    counter = counter + 1
    name = event_dict["concept:name"]
    del event_dict["concept:name"]
    timestamp = event_dict["time:timestamp"]
    del event_dict["time:timestamp"]
    rest = event_dict

    return Event(id, name, timestamp, rest)


def traceMaker(string_trace):
    '''
    :param string_trace: trace in string format
    :return: string_trace as Trace object
    '''
    # removing <\trace> and <\trace> from the string_trace
    del string_trace[0]
    del string_trace[-1]

    # parsing the name of the trace
    pattern = re.compile(r'(".*").*(".*")')
    name = [m.replace('"', '') for m in re.findall(pattern, string_trace[0])[0]][1]
    del string_trace[0]

    # find all the indices of event start and event end and making a list of it
    event_indices_list = []
    for i in range(len(string_trace)):
        if string_trace[i].strip() == '<event>':
            event_indices_list.append([i, ])
        if string_trace[i].strip() == '</event>':
            event_indices_list[-1] = [event_indices_list[-1][0], i + 1]

    # parsing events using eventMaker
    result = Trace(name)
    for i in event_indices_list:
        result.append(eventMaker(string_trace[i[0]:i[1]]))

    return result


def xesFileReader(file_path):
    '''
    Input : xes file path
    Output : a Log containing the traces
    '''
    # reading the file as list of lines
    with open(file_path) as input_file:
        content = input_file.readlines()

    # deleting all the file content except the traces
    for i in range(len(content)):
        if content[i].strip() == "<trace>":
            del content[0:i]
            del content[-1]
            break

    # making the traces list
    traces_indices = []
    trace_index = []
    for i in range(len(content)):
        if content[i].strip() == "<trace>":
            trace_index += [i]
        if content[i].strip() == "</trace>":
            trace_index += [i]
            traces_indices.append(trace_index)
            trace_index = []

    traces = []
    for i in traces_indices:
        traces.append(content[i[0]:i[1] + 1])

    result = []
    for trace in traces:
        result = result + [traceMaker(trace)]
        global counter
        counter = 0

    result_log = Log()
    result_log.traces = result
    result_log.set_symbolmapping()
    # result_log.set_symbolmapping()

    return result_log

