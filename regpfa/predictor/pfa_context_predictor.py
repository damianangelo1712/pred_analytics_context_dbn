from scipy.stats import norm
import numpy as np


class PFA:
    def __init__(self, log, states_k):
        self.numberofstates = states_k
        self.numberofsymbols = log.get_numberOfUniqueSymbols()
        self.prior = []
        self.obsmat = []
        self.transcube = []
        self.log = log

    def get_prior(self):
        return list(self.prior)

    def set_randomdistributions(self):
        # get symbol frequency
        # symbolfreq = self.log.get_startsymbolfrequency()

        # make sure alpha is never 0
        # for key,value in symbolfreq.items():
        #   if symbolfreq[key] == 0:
        #      symbolfreq[key] = 1

        prior = np.random.dirichlet(np.ones(self.numberofstates))
        self.prior = prior
        obsmat = np.random.dirichlet(np.ones(self.numberofsymbols), self.numberofstates)
        self.obsmat = obsmat
        transcube = np.random.dirichlet(np.ones(self.numberofstates), (self.numberofstates, self.numberofsymbols))
        self.transcube = transcube

    def predictProbability(self, trace):

        stateDistributionTrace = self.updatestatedistribution(trace)
        symbolDistributionTrace = []

        for i in range(0, self.log.get_numberOfUniqueSymbols() - 1):
            symbolDistributionTrace.append(0.0)
            for j in range(0, self.numberofstates - 1):
                symbolDistributionTrace[i] = symbolDistributionTrace[i] + stateDistributionTrace[j] * self.obsmat[j][i]
        return symbolDistributionTrace

    def updatestatedistribution(self, trace):
        path_ids = []
        stateDistribution = self.get_prior()
        for event in trace:
            path_ids.append(self.log.get_symbolidfromname(event))
        for i in path_ids[:-1]:
            oldStateDistribution = list(stateDistribution)
            tmpsum = 0.0
            for j in range(0, self.numberofstates):
                stateDistribution[j] = 0.0
                for k in range(0, self.numberofstates):
                    stateDistribution[j] += oldStateDistribution[k] * self.transcube[k][i][j]
                tmpsum += stateDistribution[j]
        return stateDistribution

    def predict(self, trace):
        symbolDistribution = self.predictProbability(trace)
        max_value = max(symbolDistribution)
        max_index = symbolDistribution.index(max_value)

        return self.log.get_symbolnamefromid(max_index)

    def scoreAccuracy(self):
        result = []
        for trace in self.log.traces:
            if trace.get_lasteventfrompath() == self.predict(trace.get_pathwithoutlastevent()): #TODO: workaround to use get_pathwithoutlastevent - in the future this should happen differently
                result.append(1.0)
            else:
                result.append(0.0)
        return sum(result) / len(result)
