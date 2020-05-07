# -*- coding: utf-8 -*-

from stl import mesh
# from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt 
import numpy as np
import math
from sklearn.linear_model import LinearRegression
import os
import sys
from tqdm import tqdm
import pprint


def count(arr, x, y, z, b):
    """ img: 対象画像、x,y: 画像のサイズ、b: ボックスのサイズ """
    i = j = k = 0
    b_tmp  = b
    b_tmp2 = b
    ct = 0

    j_tmp = b
    k_tmp = b
    while k < z:
        while j < y:
            while i < x:
                if (np.any(arr[i:b, j:j_tmp, k:k_tmp] == 1)):
                        # if (b_tmp2 == 100):
                        #     print("[", i, b, "]", "[", j, j_tmp, "]", "[",  k, k_tmp, "]")
                        ct += 1
                i += b_tmp
                b += b_tmp
            # print("x返し")
            j += b_tmp2
            j_tmp += b_tmp2
            b = b_tmp2
            i = 0
        # print("y返し")
        k += b_tmp2
        k_tmp += b_tmp2
        b = b_tmp2
        j_tmp = b_tmp2
        i = 0
        j = 0

    return ct # 図形が含まれていたボックスの数を返す


def min_and_max(data):
    x_arr = []
    y_arr = []
    z_arr = []
    
    for i in range(len(data)):

        x1 = data.vectors[i][0][0]
        x2 = data.vectors[i][1][0]
        x3 = data.vectors[i][2][0]

        y1 = data.vectors[i][0][1]
        y2 = data.vectors[i][1][1]
        y3 = data.vectors[i][2][1]
        
        z1 = data.vectors[i][0][2]
        z2 = data.vectors[i][1][2]
        z3 = data.vectors[i][2][2]

        x_arr.append(x1)
        x_arr.append(x2)
        x_arr.append(x3)

        y_arr.append(y1)
        y_arr.append(y2)
        y_arr.append(y3)

        z_arr.append(z1)
        z_arr.append(z2)
        z_arr.append(z3)

    x_max = max(x_arr)
    y_max = max(y_arr)
    z_max = max(z_arr)
    x_min = min(x_arr)
    y_min = min(y_arr)
    z_min = min(z_arr)

    return x_max, y_max, z_max, x_min, y_min, z_min


def calcu(array3d, a1, a2, a3, x1, x2, x3, y1, y2, y3, z1, z2, z3, x_max, y_max, z_max, x_min, y_min, z_min):

    new_x = a1*x1 + a2*x2 + a3*x3
    new_y = a1*y1 + a2*y2 + a3*y3
    new_z = a1*z1 + a2*z2 + a3*z3

    x_point = int((new_x - x_min) / 0.5) - 1
    y_point = int((new_y - y_min) / 0.5) - 1
    z_point = int((new_z - z_min) / 0.5) - 1

    if (x_point < 0):
        x_point = 0
    if (y_point < 0):
        y_point = 0
    if (z_point < 0):
        z_point = 0

    array3d[x_point][y_point][z_point] = 1

    return x_point, y_point, z_point


def different_param(data, a1, a2, a3, x_arr, y_arr, z_arr, array3d, x_max, y_max, z_max, x_min, y_min, z_min):
    
    for i in range(len(data)):
      
        x1 = data.vectors[i][0][0]
        x2 = data.vectors[i][1][0]
        x3 = data.vectors[i][2][0]

        y1 = data.vectors[i][0][1]
        y2 = data.vectors[i][1][1]
        y3 = data.vectors[i][2][1]
        
        z1 = data.vectors[i][0][2]
        z2 = data.vectors[i][1][2]
        z3 = data.vectors[i][2][2]

        x_arr.append(x1)
        x_arr.append(x2)
        x_arr.append(x3)

        y_arr.append(y1)
        y_arr.append(y2)
        y_arr.append(y3)

        z_arr.append(z1)
        z_arr.append(z2)
        z_arr.append(z3)

        x_point, y_point, z_point = calcu(array3d, a1, a2, a3, x1, x2, x3, y1, y2, y3, z1, z2, z3, x_max, y_max, z_max, x_min, y_min, z_min)


def show(data, array3d, x_max, y_max, z_max, x_min, y_min, z_min):

    np.set_printoptions(threshold=np.inf)

    print("len(data)", len(data))
    x_arr = []
    y_arr = []
    z_arr = []

    for i in tqdm(range(200)):     # stl三角形判定の精度() 
        arr = np.random.rand(3)
        arr /= np.sum(arr)
        different_param(data, arr[0], arr[1], arr[2], x_arr, y_arr, z_arr, array3d, x_max, y_max, z_max, x_min, y_min, z_min)

    
    x_max = max(x_arr)
    y_max = max(y_arr)
    z_max = max(z_arr)
    x_min = min(x_arr)
    y_min = min(y_arr)
    z_min = min(z_arr)

    return array3d


def main():

    # data = mesh.Mesh.from_file('100_100_test_mesh.stl')
    # data = mesh.Mesh.from_file('new_point9999_result.stl')
    data = mesh.Mesh.from_file('Dragon.stl')

    print(len(data.vectors))

    graph_x = []
    graph_y = []

    x_max, y_max, z_max, x_min, y_min, z_min = min_and_max(data)
    x_size = int(x_max-x_min) * 2
    y_size = int(y_max-y_min) * 2
    z_size = int(z_max-z_min) * 2
    print("x_size", x_size)
    print("y_size", y_size)
    print("z_size", z_size)

    array = np.zeros((x_size,y_size,z_size))

    array3d = show(data, array, x_max, y_max, z_max, x_min, y_min, z_min)

    # array3d = np.ones((x_size,y_size,z_size))

    grid_size = max([x_size, y_size, z_size])

    ct_1 = np.count_nonzero(array3d == 1)
    print("array_size", array3d.size)
    print("count_of_1", ct_1)

    while grid_size > 1:
        n = count(array3d, x_size, y_size, z_size, grid_size)

        graph_x.append(math.log(grid_size))
        graph_y.append(math.log(n))
        print(grid_size, n)
        print (math.log(grid_size), math.log(n))
        grid_size = int(grid_size / 2)
    
    graph_x.append(math.log(1))
    graph_y.append(math.log(ct_1))

    graph_x = np.array(graph_x).reshape((len(graph_x), 1)) # 1列にする
    graph_y = np.array(graph_y).reshape((len(graph_y), 1))

    model_lr = LinearRegression()
    model_lr.fit(graph_x, graph_y)

    plt.plot(graph_x, graph_y, 'o')
    plt.plot(graph_x, model_lr.predict(graph_x), linestyle="solid")

    # plt.xlabel("")
    # plt.ylabel("気温（℃）")

    print("回帰係数=", model_lr.coef_) # フラクタル次元
    print('決定係数 R^2： ', model_lr.score(graph_x, graph_y))

    # plt.show()

    fractal = model_lr.coef_[0][0] 

    print("Fractal : ", fractal)


if __name__ == "__main__":
    main()