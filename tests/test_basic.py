# -*- coding: utf-8 -*-

#from .context import regpfa

import unittest
import os
import regpfa.datain.logparsers
import regpfa.inputParsing.xesFileParser
import regpfa.predictor.pfa_predictor
import regpfa.predictor.dbn_predictor


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

#    def test_load_xes_file(self):
#        dirname = os.path.dirname(__file__)
#        filename = os.path.join(dirname, 'test.xes')
#        with open(filename) as input_file:
#            log = regpfa.models.eventlog.logparsers.parsexes(input_file)
#
#
#     def test_run_pfa_predictor(self):
#         dirname = os.path.dirname(__file__)
#         filename = os.path.join(dirname, 'test2.xes')
#         with open(filename) as input_file:
#            log = regpfa.models.eventlog.logparsers.parsexes(input_file)
#         accuracy = []
#         for i in range(0,10):
#             pfa = regpfa.predictor.pfa_predictor.PFA(log, 5)
#             pfa.set_randomdistributions()
#             accuracy.append(pfa.scoreAccuracy())
#         print('Result: ', sum(accuracy)/len(accuracy))

    def test_run_dbn_predictor(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'test.xes')
        with open(filename) as input_file:
         log = regpfa.datain.logparsers.parsexes(input_file)
          #log= regpfa.inputParsing.xesFileParser.xesFileReader(filename)
        #print(log.get_logwithoutnumericattr().dtypes)
        print(log.nocontextelements)

        accuracy = []
        for i in range(0,10):
            pfa = regpfa.predictor.pfa_predictor.PFA(log, 1)
            pfa.set_randomdistributions()
            accuracy.append(pfa.scoreAccuracy())
        print('Result: ', sum(accuracy)/len(accuracy))



if __name__ == '__main__':
    unittest.main()