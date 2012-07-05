#!/usr/bin/python
# Back-Propagation Neural Networks
# 
# Written in Python.  See http://www.python.org/
#
# Neil Schemenauer <nascheme@enme.ucalgary.ca>

import math
import random as random

# Local imports
import util


random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b, random=random.random):
        return (b-a)*random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
        m = []
        for i in range(I):
                m.append([fill]*J)
        return m

class NN(object):
#    print 'class NN'    
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-2.0, 2.0)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum   
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
#        print 'update', inputs
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.ni-1):
            #self.ai[i] = 1.0/(1.0+math.exp(-inputs[i]))
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                 sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = 1.0/(1.0+math.exp(-sum))

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = 1.0/(1.0+math.exp(-sum))

        return self.ao[:]


    def backPropagate(self, targets, N, M):
#        print N, M
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
#        print self.no
        for k in range(self.no):
            ao = self.ao[k]
            output_deltas[k] = ao*(1-ao)*(targets[k]-ao)

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            sum = 0.0
            for k in range(self.no):
                sum = sum + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = self.ah[j]*(1-self.ah[j])*sum

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
        for p in patterns:
            print('%s -> %s' % (p[0], self.update(p[0])))

    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print('')
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=2000, N=0.5, M=0.1):
# N: learning rate
# M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            #if i % 100 == 0:
            #    print i, 'error %-14f' % error


def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, two hidden, and two output nodes
    n = NN(2, 3, 1)
    # train it with some patterns
    n.train(pat, 5000)
    # test it
    #n.test(pat)

def time(fn, *args):
    import time, traceback
    begin = time.time()
    result = fn(*args)
    end = time.time()
    return result, end-begin

def test_bpnn(iterations):
    times = []
    for _ in range(iterations):
        result, t = time(demo)
        times.append(t)
    return times

main = test_bpnn

if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of a neural network."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, test_bpnn)
