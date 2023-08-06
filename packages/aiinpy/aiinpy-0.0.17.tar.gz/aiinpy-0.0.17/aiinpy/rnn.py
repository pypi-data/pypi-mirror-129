import numpy as np
from .activation import *

class rnn:
  def __init__(self, outshape, Type, outactivation=stablesoftmax(), hidshape=64, learningrate=0.05, inshape=None):
    self.learningrate, self.Type, self.outactivation = learningrate, Type, outactivation
    self.inshape, self.hidshape, self.outshape = inshape, hidshape, outshape
    
    if inshape is not None:
      self.weightsinToHid = np.random.uniform(-0.005, 0.005, (hidshape, inshape))

    self.weightsHidToHid = np.random.uniform(-0.005, 0.005, (hidshape, hidshape))
    self.Hidbiases = np.zeros(hidshape)

    self.weightsHidToout = np.random.uniform(-0.005, 0.005, (outshape, hidshape))
    self.outbiases = np.zeros(outshape)

  def __copy__(self):
    return type(self)(self.outshape, self.Type, self.outactivation, self.hidshape, self.learningrate, self.inshape)

  def modelinit(self, inshape):
    self.inshape = inshape
    self.weightsinToHid = np.random.uniform(-0.005, 0.005, (hidshape, inshape))
    return self.outshape

  def forward(self, input):
    self.input = input
    self.Hid = np.zeros((len(self.input) + 1, self.hidshape))
    
    if self.Type == 'ManyToOne':
      for i in range(len(input)):
        self.Hid[i + 1, :] = tanh().forward(self.weightsinToHid @ input[i] + self.weightsHidToHid @ self.Hid[i, :] + self.Hidbiases)

      self.out = self.outactivation.forward(self.weightsHidToout @ self.Hid[len(input), :] + self.outbiases)
    
    elif self.Type == 'ManyToMany':
      self.out = np.zeros((len(self.input), self.outshape))

      for i in range(len(input)):
        self.Hid[i + 1, :] = tanh().forward(self.weightsinToHid @ input[i] + self.weightsHidToHid @ self.Hid[i, :] + self.Hidbiases)
        self.out[i, :] = self.outactivation.forward(self.weightsHidToout @ self.Hid[i + 1, :] + self.outbiases)

    return self.out

  def backward(self, outError):
    weightsinToHidΔ = np.zeros(self.weightsinToHid.shape)
    weightsHidToHidΔ = np.zeros(self.weightsHidToHid.shape)
    HidbiasesΔ = np.zeros(self.Hidbiases.shape)

    if self.Type == 'ManyToOne':
      outGradient = np.multiply(self.outactivation.backward(self.out), outError)

      weightsHidTooutΔ = np.outer(outGradient, self.Hid[len(self.input)].T)
      outbiasesΔ = outGradient

      HidError = self.weightsHidToout.T @ outError

      for i in reversed(range(len(self.input))):
        HidGradient = np.multiply(tanh().backward(self.Hid[i + 1]), HidError)

        HidbiasesΔ += HidGradient
        weightsHidToHidΔ += np.outer(HidGradient, self.Hid[i].T)
        weightsinToHidΔ += np.outer(HidGradient, self.input[i].T)

        HidError = self.weightsHidToHid.T @ HidGradient

    elif self.Type == 'ManyToMany':
      weightsHidTooutΔ = np.zeros(self.weightsHidToout.shape)
      outbiasesΔ = np.zeros(self.outbiases.shape)

      HidError = self.weightsHidToout.T @ outError[len(self.input) - 1]

      for i in reversed(range(len(self.input))):
        HidGradient = np.multiply(tanh().backward(self.Hid[i + 1]), HidError)
        outGradient = np.multiply(self.outactivation.backward(self.out[i]), outError[i])

        weightsinToHidΔ += np.outer(HidGradient, self.input[i].T)
        weightsHidToHidΔ += np.outer(HidGradient, self.Hid[i].T)
        HidbiasesΔ += HidGradient

        weightsHidTooutΔ += np.outer(outGradient, self.Hid[i].T)
        outbiasesΔ += outGradient

        HidError = self.weightsHidToHid.T @ HidGradient + self.weightsHidToout.T @ outError[i]

    self.weightsinToHid += self.learningrate * np.clip(weightsinToHidΔ, -1, 1)
    self.weightsHidToHid += self.learningrate * np.clip(weightsHidToHidΔ, -1, 1)
    self.Hidbiases += self.learningrate * np.clip(HidbiasesΔ, -1, 1)

    self.weightsHidToout += self.learningrate * np.clip(weightsHidTooutΔ, -1, 1)
    self.outbiases += self.learningrate * np.clip(outbiasesΔ, -1, 1)