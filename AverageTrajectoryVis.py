import numpy as np
import matplotlib.pyplot as plt

from model import model
from summary import summary

b0 = 0.0000001; g0 = 0.4

#summ = summary(np.load('test_large.npy'), mod=model(0.0000001, .0000001, 11, 0.5, 0.001, 5, .9))
summ = summary(np.load('modelTests/test_large.npy'), mod=model(b0, b0, 11, g0, 0.05, 5, .9))

run = np.load('modelTests/lstAv_large_cu_new.npy', allow_pickle=True)

summ.visAverages(run, savedirec='/tmp/ramdisk', show=False)
summ.visEndAverages(run, savedirec='/tmp/ramdisk', show=False)
