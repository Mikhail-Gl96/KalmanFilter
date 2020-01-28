import numpy as np
import matplotlib.pyplot as plt

import WhiteNoise as WhiteNoise

# wn = WhiteNoise.WhiteNoise(0, 1, 1000)
# wn.white_noise()
# samples = wn.getSamples()
#
# x = np.pi
# # y = [0:1:0.01]
# parts = 10
# i = np.linspace(-1, parts * x + 1, 1000)
# sin = []
# for y in i:
#     sinIdeal = np.sin(y)
#     sin.append(sinIdeal)
# print(sin)
# plt.plot(sin + samples/parts*2)
# plt.show()


class IdealModel:
    def __init__(self, input_data):
        self.input_data = input_data
        self.parts = input_data[0]
        self.len = input_data[1]

        self.mean = None
        self.std = None
        self.num_parts = None
        self.noise_data_samples = None

        self.result_data = None
        self.noise_data = None
        self.result_IdealModel_and_WhiteNoise = None

    def make_sin(self):
        local_input_data = np.linspace(-1, np.pi * self.parts, self.len)
        self.result_data = []
        for y in local_input_data:
            sinIdeal = np.sin(y)
            self.result_data.append(sinIdeal)
        return self.result_data

    def getIdealModelSample(self):
        return self.result_data

    def addWhiteNoise_to_IdealModel(self, mean=0, std=1, num_parts=1000):
        self.mean = mean
        self.std = std
        self.num_parts = num_parts
        wn = WhiteNoise.WhiteNoise(self.mean, self.std, self.num_parts)
        wn.white_noise()
        samples = wn.getSamples()
        self.noise_data_samples = samples
        self.noise_data = samples/self.parts*2
        self.result_IdealModel_and_WhiteNoise = self.result_data + self.noise_data
        return self.result_IdealModel_and_WhiteNoise

    def get_IdealNoisedResult(self):
        return self.result_IdealModel_and_WhiteNoise

    def change_noise_level(self, noise_level=1):
        self.noise_data = self.noise_data_samples / self.parts * noise_level
        self.result_IdealModel_and_WhiteNoise = self.result_data + self.noise_data
        return self.result_IdealModel_and_WhiteNoise
