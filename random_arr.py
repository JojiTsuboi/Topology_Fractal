# -*- coding: utf-8 -*-

import random
import numpy as np
import csv
import itertools

def fractal(individual, i):
    number = i

    file_name = "point.bdf"
    param = "0.01_smooth1.0.txt"
 
    force_pos = []
    # pos_arr = [12098, 24138, 36178, 48218, 60258, 12156, 24196, 36236, 48276, 60316]
    # pos_arr = [12, 241, 361, 482, 602, 121, 241, 362, 482, 603]     # test

    force_support = list()
    
    with open('force.csv') as f:
        read = csv.reader(f)
        for row in read:
            force_support.append(row)


    for i in range(52):
        if individual[i] == 1:
            force_support_tmp = force_support[i][:]
            c = list()
            for k in range(4):
                if((str(force_support_tmp[k]).isdigit()) == True):
                    c.append(int(force_support_tmp[k]))
            force_pos.append(c)

    force_pos = list(itertools.chain.from_iterable(force_pos))

    with open(file_name, encoding="cp932") as f:
        data = f.readlines()

    x = 1.0
    y = 0.0
    z = 0.0

    insert_line_to_bdf = 16    # bdfファイルにforceを追記する行

    np.set_printoptions(threshold=np.inf)

    for force_pos in force_pos:

        force_pos_tmp = force_pos

        # 表面のforce
        if (len(str(force_pos)) == 2): 
            data.insert(insert_line_to_bdf, "FORCE          2      %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1
        elif (len(str(force_pos)) == 3):
            data.insert(insert_line_to_bdf, "FORCE          2     %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1
        elif (len(str(force_pos)) == 4):
            data.insert(insert_line_to_bdf, "FORCE          2    %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1
        elif (len(str(force_pos)) == 5):
            data.insert(insert_line_to_bdf, "FORCE          2   %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1

        # 裏面のforce
        force_pos = force_pos_tmp - 1
        if (len(str(force_pos)) == 2): 
            data.insert(insert_line_to_bdf, "FORCE          2      %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1
        elif (len(str(force_pos)) == 3):
            data.insert(insert_line_to_bdf, "FORCE          2     %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1
        elif (len(str(force_pos)) == 4):
            data.insert(insert_line_to_bdf, "FORCE          2    %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1
        elif (len(str(force_pos)) == 5):
            data.insert(insert_line_to_bdf, "FORCE          2   %s       01.000000%8s%8s%8s\n" % (force_pos, x, y, z))
            insert_line_to_bdf += 1

    file_name_to_save = "../bdf/new_point" + number + ".bdf"
    file_name_to_fractal = "../bdf/new_point" + number + "_result" + ".bdf"
    force_bat_name = "../bat/force" + number + ".bat"
    fractal_bat_name = "../bat/fractal" + number + ".bat"


    with open(file_name_to_save, mode="w", encoding="cp932") as f:
        f.writelines(data)

    with open(force_bat_name, mode='w') as f:
        f.write('\"C:\\Program Files\\Quint\\OPTISHAPE-TS2019\\optishape-tf\"	\"param\\%s\"	\"%s\" > nul 2>&1\n' % (param, file_name_to_save))

    with open(fractal_bat_name, mode='w') as f:
        f.write('C:\\Users\\kumanomi\\AppData\\Local\\Programs\\Python\\Python37\\python.exe ..\\Program\\result_fractal.py \"%s\"\n' % (file_name_to_fractal))



def main():
    ind = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0]

    fractal(ind, "9999")

if __name__ == "__main__":
    main()