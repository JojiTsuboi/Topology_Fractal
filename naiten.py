   
# -*- coding: utf-8 -*-

from stl import mesh
# from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt 
import numpy as np
import math
from sklearn.linear_model import LinearRegression
import os
import sys

def main():

    arr = np.random.rand(3)

    print(arr)
    print(np.sum(arr))

    arr /= np.sum(arr)

    print(arr)
    print(np.sum(arr))


if __name__ == "__main__":
    main()