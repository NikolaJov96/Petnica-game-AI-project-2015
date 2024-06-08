#
# Imports
#
import numpy as np

# Transfer functions
def sgm(x, Derivative=False):
    if not Derivative:
        return 1 / (1+np.exp(-x))
    else:
        out = sgm(x)
    return out * (1.0 - out)

def linear(x, Derivative=False):
    if not Derivative:
        return x
    else:
        return 1.0

def gaussian(x, Derivative=False):
    if not Derivative:
        return np.exp(-x**2)
    else:
        return -2*x*np.exp(-x**2)
    
def tg(x, Derivative=False):
    if not Derivative:
        return np.tanh(x)
    else:
        return 1.0 - np.tanh(x)**2


class BackPropagationNetwork:
    """A back-propagation network"""

    #
    # Class members
    #
    layerCount = 0
    shape = None
    weights = []
    transferFunc = sgm

    #
    # Class methods
    #
    def __init__(self, layerSize):
        """Initialize the network"""

        # Layer info
        self.layerCount = len(layerSize) - 1
        self.shape = layerSize

        # Data from last Run
        self._layerInput = []
        self._layerOutput = []
        self._previousWeightDelta = []

        # Create the weight arrays
        for (l1,l2) in zip(layerSize[:-1], layerSize[1:]):
            self.weights.append(np.random.normal(scale=0.1, size = (l2, l1+1)))
            self._previousWeightDelta.append(np.zeros((l2, l1+1)))

    #
    # Run method
    #
    def Run(self, inpu):
        """Run the network based on the input data"""

        lnCases = inpu.shape[0]

        # Clear out the previous intermediate value lists
        self._layerInput = []
        self._layerOutput = []

        # Run it!
        for index in range(self.layerCount):
            if index == 0:
                layerInput = self.weights[0].dot(np.vstack([inpu.T, np.ones([1, lnCases])]))
            else:
                layerInput = self.weights[index].dot(np.vstack([self._layerOutput[-1], np.ones([1, lnCases])]))
            self._layerInput.append(layerInput)
            self._layerOutput.append(tg(layerInput))

        return self._layerOutput[-1].T

    #
    # Trainepoch method
    #
    def TrainEpoch(self, inpu, target, trainingRate = 0.2, momentum = 0.5):
        """This method trains the network for one epoch"""

        delta = []
        lnCases = inpu.shape[0]

        #First run the network
        self.Run(inpu)

        # Calculate our deltas
        for index in reversed(range(self.layerCount)):
            if index == self.layerCount - 1:
                # Compare to the target values
                output_delta = self._layerOutput[index] - target.T
                error = np.sum(output_delta**2)
                delta.append(output_delta * tg(self._layerInput[index], True))
            else:
                # Compare to the following layer's delta
                delta_pullback = self.weights[index-1].T.dot(delta[-1])
                delta.append(delta_pullback[:-1, :] * tg(self._layerInput[index], True))

        # Compute weight deltas
        for index in range(self.layerCount):
            delta_index = self.layerCount - 1 - index

            if index == 0:
                layerOutput = np.vstack([inpu.T, np.ones([1, lnCases])])
            else:
                layerOutput = np.vstack([self._layerOutput[index - 1], np.ones([1, self._layerOutput[index-1].shape[1]])])

            curWeightDelta = np.sum(layerOutput[None,:,:].transpose(2,0,1) * delta[delta_index][None,:,:].transpose(2,1,0), axis = 0)

            weightDelta = trainingRate*curWeightDelta + momentum*self._previousWeightDelta[index]

            self.weights[index] -= weightDelta

            self._previousWeightDelta[index] = weightDelta

        return error

        
#
# If run as a script, create a test object
#
if __name__ == "__main__":
    bpn = BackPropagationNetwork((201, 201, 1))
    #print(bpn.shape)
    #print(bpn.weights)

    #lvInput =  np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
    #lvTarget = np.array([[0.05], [0.05], [0.95], [0.95]])
    datLoad = np.load('trainingFile.npy')
    lInput = []
    lTarget = []
    for iterat in datLoad:
        lInput.append(np.array(iterat[0]).ravel().tolist())
        if iterat[2] == 'a': lInput[-1].append(1)
        elif iterat[2] == 'd': lInput[-1].append(2)
        elif iterat[2] == 's': lInput[-1].append(3)
        if iterat[1] == -1: lTarget.append(-0.9)
        elif iterat[1] == 0: lTarget.append(0)
        elif iterat[1] == 1: lTarget.append(0.9)
    lvInput = np.array(lInput)
    lvTarget = np.array(lTarget)
    print 'Steps: ', len(lvInput), len(lvInput[0])

    lnMax = 100000
    lnErr = 0.00001
    for i in range(lnMax-1):
        err = bpn.TrainEpoch(lvInput, lvTarget, trainingRate = 0.2, momentum=0)
        if i % 1 == 0:
            print ("Iteration {0}\tError: {1:0.6f}".format(i, err))
        if err <= lnErr:
            print ("Minimum error reachedat iteration {0}".format(i))
            break

    # Display output
    lvOutput = bpn.Run(lvInput)

    #for i in range(lvInput.shape[0]):
    #    print ("Input: {0} Output: {1}".format(lvInput[i], lvOutput[i]))







        
