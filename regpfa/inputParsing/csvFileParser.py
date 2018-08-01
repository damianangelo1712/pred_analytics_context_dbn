import csv
import regpfa.models.eventlog.log as log_class
from regpfa.models.eventlog import Event, Trace, Log

counter = -1  # counts for the event id assignment
trace_name = ''
event_name = ''
time_record = ''


def eventMaker(input_dict):
    '''
    makes an Event class object
    :param input_dict: one row from csv.reaer
    :return: Event object made from the 'row'
    '''
    del input_dict[trace_name]  # deletes trace_name key as it is unnecessary
    name = input_dict[event_name]
    del input_dict[event_name]
    time_stamp = input_dict[time_record]
    del input_dict[time_record]
    further_attributes = input_dict
    global counter
    counter = counter + 1
    return Event(counter, name, time_stamp, further_attributes)


def csvFileParser(file_name):
    '''
    makes a Log object out of the given input csv file
    :param file_name: path of the csv file
    :return: Log object containing the traces read from the csv file
    '''

    # reading the row name for case_name, event_name and time_span imitating Celonis software.
    # For further information on how Celonis imports a spreadsheet into it, please visit the following link
    # https://www.youtube.com/watch?v=af-fyfuh88Y

    global trace_name, event_name, time_record
    while True:
        try:
            trace_name, event_name, time_record = input(
                'Enter the names of the columns for Trace Name, Event Name and Time Stamp respectively separated by spaces\n').split()
            trace_name.strip()
            event_name.strip()
            time_record.strip()
            with open(file_name, newline='') as csvfile:
                reader = csv.reader(csvfile)
                row1 = next(reader)
            if not (trace_name in row1 and event_name in row1 and time_record in row1):
                raise NameError('Columns not found')
            break
        except FileNotFoundError:
            file_name = input('The input file is not found\nTry entering a new file name including the path\n')
        except ValueError:
            print(
                'You did not enter all the necessary input column names: Trace Name, Event Name, Time Stamp in the right format.\nPlease try again\n')
        except NameError:
            print('The column names are not found in the given csv file.\nTry again')


    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        traces = []
        for row in reader:
            if not traces:
                trace = Trace(row[trace_name])
                trace.events = [eventMaker(row)]
                traces = traces + [trace, ]
                continue

            trace_found = False
            for i in traces:
                if i.name == row[trace_name]:
                    trace_found = True
                    i.append(eventMaker(row))
                    break

            if not trace_found:
                global counter
                counter = -1
                trace = Trace(row[trace_name])
                trace.events = [eventMaker(row)]
                traces = traces + [trace, ]

    result_log = Log()
    result_log.traces = traces
    result_log.symbolmapping = result_log.set_symbolmapping()
    return result_log


# if __name__ == "__main__":
#     x = csvFileParser('../test/test.csv')
