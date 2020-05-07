   
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

    graph_x = []
    graph_y = []
    

    graph_x.append(math.log(200))
    graph_y.append(math.log(1))
    graph_x.append(math.log(100))
    graph_y.append(math.log(8))
    graph_x.append(math.log(50))
    graph_y.append(math.log(64))
    graph_x.append(math.log(25))
    graph_y.append(math.log(512))
    graph_x.append(math.log(12))
    graph_y.append(math.log(4096))
    graph_x.append(math.log(6))
    graph_y.append(math.log(32768))
    graph_x.append(math.log(3))
    graph_y.append(math.log(262144))
    graph_x.append(math.log(1))
    graph_y.append(math.log(2097152))

    print(graph_x)
    print(graph_y)

    graph_x = np.array(graph_x).reshape((len(graph_x), 1)) # 1列にする
    graph_y = np.array(graph_y).reshape((len(graph_y), 1))

    model_lr = LinearRegression()
    model_lr.fit(graph_x, graph_y)

    plt.plot(graph_x, graph_y, 'o')
    plt.plot(graph_x, model_lr.predict(graph_x), linestyle="solid")
    plt.show()

    fractal = model_lr.coef_[0][0] 

    print("Fractal : ", fractal)

if __name__ == "__main__":
    main()