import numpy as np

'''
Few important notations you should know:
Z - various possible states of the PetriNet (N)
X - various possible transitions/Observations possible in PetriNet (M)
pi - probability distribution of initial states.

All these variables together are called HMM parameters denoted by λ 
'''


class HMM_predictor:
    def __init__(self, log):
        self.numberOfSymbols = log.get_numberOfUniqueSymbols()  # Observations/Transitions possible
        self.log = log
        self.transition_matrix = []  # A
        self.emission_matrix = []  # B
        self.initial_probability_matrix = []  # pi

    def setTransitionMatrix(self):
        '''
        Creates a Transition Matrix of size (numberOfStates, numberOfStates) and sets to the data member Transition
        Matrix
        :return: Transition Matrix
        '''
        self.transition_matrix = np.random.rand(self.numberOfStates, self.numberOfStates)
        self.transition_matrix = self.transition_matrix / self.transition_matrix.sum(axis=1)[:, None]
        return self.transition_matrix

    def setEmissionMatrix(self):
        '''
        creates a random emission matrix and sets it to self.emission_matrix
        :return: emission_matrix
        '''
        self.emission_matrix = np.random.rand(self.numberOfStates, self.numberOfSymbols)
        self.emission_matrix = self.emission_matrix / self.emission_matrix.sum(axis=1)[:, None]
        return self.emission_matrix

    def setInitialProbabilityMatrix(self):
        '''
        sets random probailities to intial probabilities called as "pi"
        :return: initial_probability_matrix
        '''
        self.initial_probability_matrix = np.random.rand(self.numberOfStates)
        return self.initial_probability_matrix

    ################## Evaluation functions #########################

    '''
    The below functions help in evaluating the probability of that a given sequence of observations {X1,X2,X3....} 
    happens given all the HMM parameters.  We have two algorithms called forward algorithm and backward algorithm
    '''

    def forward(self, obs_seq):
        '''
        Forward algorithm
        :param obs_seq: sequence of observations in list or tuple format
        :return: probability distribution of the sequence of observations
        '''
        T = len(obs_seq)
        N = self.numberOfStates
        alpha = np.zeros((T, N))
        alpha[0] = self.initial_probability_matrix[0] * self.emission_matrix[:, obs_seq[0]]
        for t in range(1, T):
            alpha[t] = alpha[t - 1].dot(self.transition_matrix) * self.emission_matrix[:, obs_seq[t]]
        return alpha

    def likelihood(self, obs_seq):
        # returns log P(Y)
        # using the forward part of the forward-backward algorithm
        return self.forward(self, obs_seq)[-1].sum()

    def backward(self, obs_seq):
        '''
        Backward algorithm
        :param obs_seq: sequence of observations in list or tuple format
        :return: probability distribution of the sequence of observations
        '''
        N = self.numberOfStates
        T = len(obs_seq)

        beta = np.zeros((N, T))
        beta[:, -1:] = 1

        for t in reversed(range(T - 1)):
            for n in range(N):
                beta[n, t] = np.sum(
                    beta[:, t + 1] * self.transition_matrix[n, :] * self.emission_matrix[:, obs_seq[t + 1]])

        return beta

    def gamma(self, obs_seq):
        '''
        Posterior probability - define posterior probability \gamma_t(i)=P(s_t=i | Y, λ)γ t(i)=P(s t=i∣Y,λ) the probability of
        being in state s_t = i  t=i at time t given the observation Y and the model λ.
        :param obs_seq: tuple or list of observations/transitions
        :return: posetrior probability
        '''
        alpha = self.forward(self, obs_seq)
        beta = self.backward(self, obs_seq)
        obs_prob = self.likelihood(self, obs_seq)
        return np.dot(alpha, beta) / obs_prob

    ################### Decoding Functions ###########################

    ''' These algorithms given HMM parameters and a observation sequence try to predict what the states of the PetriNet
    would look like.  The algorithm in use is called Viterbi Algorithm.
    '''

    def viterbi(self, obs_seq):
        # returns the most likely state sequence given observed sequence x
        # using the Viterbi algorithm
        T = len(obs_seq)
        N = self.numberOfStates
        delta = np.zeros((T, N))
        psi = np.zeros((T, N))
        delta[0] = self.initial_probability_matrix[0] * self.emission_matrix[:, obs_seq[0]]
        for t in range(1, T):
            for j in range(N):
                delta[t, j] = np.max(delta[t - 1] * self.transition_matrix[:, j]) * self.emission_matrix[j, obs_seq[t]]
                psi[t, j] = np.argmax(delta[t - 1] * self.transition_matrix[:, j])

        # backtrack
        states = np.zeros(T, dtype=np.int32)
        states[T - 1] = np.argmax(delta[T - 1])
        for t in range(T - 2, -1, -1):
            states[t] = psi[t + 1, states[t + 1]]
        return states

# # the actual predictor
# def hmm_predictor():
#     # choosing random values for states number and transitions number
#     no_of_states = 3  # np.random.randint(1, 1000)
#     no_of_transitions = 3  # np.random.randint(1, 1000)
#
#     # creating necessary transition and emision matrices
#     transition_matrix = createTransitionMatrix(no_of_states)
#     emission_matrix = createEmissionMatrix((no_of_states, no_of_transitions))
#
#     # creating initial distribution
#     initial_probability_dist = np.zeros(no_of_states)
#     initial_probability_dist[0] = initial_probability_dist[-1] = 1
#
#     n = no_of_states
#
#     # forward algortihm
#
#     alpha = [initial_probability_dist[0] * emission_matrix[0][0]]  # here alpha[k] denotes log_e [ P(Z_k, X_{1:k}) ]
#     for k in range(1, n):
#         sum = 0
#         for i in range(1, no_of_states):
#             sum = sum + alpha[k] * emission_matrix[k][k] * transition_matrix[i - 1][k]
#         alpha = alpha + [sum]
#
#     # Backward algorithm
#     k = n - 2
#     beta = [0] * n
#     beta[-1] = 1
#     while k >= 0:
#         sum = 0
#         for i in range(k + 1, no_of_states):
#             sum = sum + beta[k + 1] * emission_matrix[k + 1][i] * transition_matrix[i][k]
#         beta[k] = sum
#         k = k - 1
#
