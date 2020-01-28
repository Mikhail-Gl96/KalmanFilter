import numpy
import matplotlib.pyplot as plt

# mean = 0
# std = 1
# num_samples = 1000
# samples = numpy.random.normal(mean, std, size=num_samples)
#
# plt.plot(samples)
# plt.show()


# def white_noise(mean=0, std=1, num_samples=1000):
#     samples = numpy.random.normal(mean, std, size=num_samples)
#     return samples


class WhiteNoise:
    def __init__(self, mean=0, std=1, num_samples=1000):
        self.mean = mean
        self.std = std
        self.num_samples = num_samples
        self.samples = None

    def getMean(self):
        return self.mean

    def getStd(self):
        return self.std

    def getNum_samples(self):
        return self.num_samples

    def setMean(self, mean):
        self.mean = mean

    def setStd(self, std):
        self.std = std

    def setNum_samples(self, num):
        self.num_samples = num

    def white_noise(self):
        self.clearSample()
        self.samples = numpy.random.normal(self.mean, self.std, size=self.num_samples)
        return self.samples

    def getSamples(self):
        return self.samples

    def clearSample(self):
        self.samples = None

