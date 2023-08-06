import numpy as np
from .activation import *

class conv:
  def __init__(self, filtershape, learningrate, activation=identity, padding=False, stride=(1, 1), inshape=None):
    self.learningrate, self.activation, self.padding, self.stride = learningrate, activation, padding, stride
    self.inshape = inshape

    self.filtershape = filtershape
    self.Filter = np.random.uniform(-0.25, 0.25, (self.filtershape))
    self.bias = np.zeros(self.filtershape[0])

    if inshape is not None:
      if len(inshape) == 2:
        inshape = tuple([self.filtershape[0]]) + inshape
      if padding == True:
        inshape = (inshape[0], inshape[1] + self.filtershape[1] - 1, inshape[2] + self.filtershape[2] - 1)
      self.outshape = tuple([filtershape[0], int((inshape[1] - filtershape[1] + 1) / self.stride[0]), int((inshape[2] - filtershape[2] + 1) / self.stride[1])])
      self.out = np.zeros(self.outshape)

  def __copy__(self):
    return type(self)(self.filtershape, self.learningrate, self.activation, self.padding, self.stride, self.inshape)

  def modelinit(self, inshape):
    if len(inshape) == 2:
      inshape = tuple([self.filtershape[0]]) + inshape
    if self.padding == True:
      inshape = (inshape[0], inshape[1] + self.filtershape[1] - 1, inshape[2] + self.filtershape[2] - 1)
    self.outshape = tuple([self.filtershape[0], int((inshape[1] - self.filtershape[1] + 1) / self.stride[0]), int((inshape[2] - self.filtershape[2] + 1) / self.stride[1])])
    self.out = np.zeros(self.outshape)

    return self.outshape

  def SetSlopeForLeakyReLU(self, Slope):
    LeakyReLU.Slope = Slope

  def forward(self, input):
    self.input = input
    if(input.ndim == 2):
      self.input = np.stack(([self.input] * self.filtershape[0]))
    if (self.padding == True):
      self.input = np.pad(self.input, int((len(self.Filter[0]) - 1) / 2), mode='constant')[1 : self.filtershape[0] + 1]

    for i in range(0, self.outshape[1], self.stride[0]):
      for j in range(0, self.outshape[2], self.stride[1]):
        self.out[:, i, j] = np.sum(np.multiply(self.input[:, i : i + self.filtershape[1], j : j + self.filtershape[2]], self.Filter), axis=(1, 2))

    self.out += self.bias[:, np.newaxis, np.newaxis]
    self.out = self.activation.forward(self.out)

    return self.out
  
  def backward(self, outError):
    FilterΔ = np.zeros(self.filtershape)
    
    outGradient = self.activation.backward(self.out) * outError

    for i in range(0, self.outshape[1], self.stride[0]):
      for j in range(0, self.outshape[2], self.stride[1]):
        FilterΔ += self.input[:, i : i + self.filtershape[1], j : j + self.filtershape[2]] * outGradient[:, i, j][:, np.newaxis, np.newaxis]
    
    self.bias += np.sum(outGradient, axis=(1, 2)) * self.learningrate
    self.Filter += FilterΔ * self.learningrate

    # in Error
    RotFilter = np.rot90(np.rot90(self.Filter))
    PaddedError = np.pad(outError, self.filtershape[1] - 1, mode='constant')[self.filtershape[1] - 1 : self.filtershape[0] + self.filtershape[1] - 1, :, :]
    
    self.inError = np.zeros(self.inshape)
    if np.ndim(self.inError) == 3:
      for i in range(int(self.inshape[1] / self.stride[0])):
        for j in range(int(self.inshape[2] / self.stride[1])):
         self.inError[:, i * self.stride[0], j * self.stride[1]] = np.sum(np.multiply(RotFilter, PaddedError[:, i:i + self.filtershape[1], j:j + self.filtershape[2]]), axis=(1, 2))
       
    if np.ndim(self.inError) == 2:
      for i in range(int(self.inshape[0] / self.stride[0])):
        for j in range(int(self.inshape[1] / self.stride[1])):
         self.inError[i * self.stride[0], j * self.stride[1]] = np.sum(np.multiply(RotFilter, PaddedError[:, i:i + self.filtershape[1], j:j + self.filtershape[2]]))

    return self.inError