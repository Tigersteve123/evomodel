import numpy as np
import matplotlib.pyplot as plt

from model import model
from summary import summary

summ = summary(np.load('test_large.npy'), mod=model(0.0000001, .0000001, 11, 0.5, 0.001, 5, .9))

run = np.load('lstAv_large_cu.npy', allow_pickle=True)

summ.visAverages(run, savedirec='/tmp/ramdisk', show=False)
summ.visEndAverages(run, savedirec='/tmp/ramdisk', show=False)
