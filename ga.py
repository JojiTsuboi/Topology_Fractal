# -*- coding: utf-8 -*-

import random
from deap import base
from deap import creator
from deap import tools
import random_arr
import os
import csv
import shutil
from scoop import futures
from concurrent.futures import ThreadPoolExecutor
import time
import concurrent.futures

path = "../bat/fractal_text.txt"
param = "0.01_smooth1.0.txt"

var_num = 52    # 変数
target_fractal = 1.4490904390896722

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, var_num)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

database = {}

def write_log(str1, str2):
    
    with open('../ga_log.txt', 'a') as f:
        f.write(str1 + " : " + str2 + "\n") 

def change_decimal_ind(individual):
    num = str(individual[0])
    for i in range(1,var_num):
        num = num + str(individual[i])
    decimal_ind = int(num,2)

    return decimal_ind

def calc_fractal(number, individual, decimal_ind):
    if (decimal_ind in database) == True:
        with open('../ga_log.txt', 'a') as f:
            f.write(str(individual) + " : db" + str(database[decimal_ind]) + "\n")
        return database[decimal_ind],
    else:
        fractal_bat = "fractal" + number + ".bat"
        os.chdir('../bat')
        os.system(fractal_bat)
        os.chdir('../Program')

        with open(path) as f:
            s = f.read().splitlines()
        square_error = (target_fractal - float(s[0])) ** 2
        write_log(str(individual), str(s[0]))
        bdf_copy_name = "../bdf/new_point" + number +"_result.bdf"
        bdf_file_name = "../result/" + str(decimal_ind) + "_" + str(s[0]) +  ".bdf"
        shutil.copyfile(bdf_copy_name, bdf_file_name)
        database[decimal_ind] = float(s[0])

    return square_error,

def calc_topology(number):
    force_bat = "force" + number + ".bat"
    os.chdir('../bat')
    os.system(force_bat)
    os.chdir('../Program')


def eval_fractal(pop):

    fitness_arr = []

    shutil.rmtree('../bdf')
    time.sleep(1)   # error出るんでちょっと待つ
    os.makedirs('../bdf', exist_ok=True)

    decimal_pop = list(map(change_decimal_ind, pop))    # 10進数化

    for i in range(len(pop)):
        if (decimal_pop[i] in database) == False:
            random_arr.fractal(pop[i], str(i))

    executor = concurrent.futures.ProcessPoolExecutor(max_workers=4)
    
    for i in range(len(pop)):
        futures = executor.submit(calc_topology, str(i))
    
    executor.shutdown()

    for i in range(len(pop)):
        square_error = calc_fractal(str(i), pop[i], decimal_pop[i])
        print("error", square_error)
        fitness_arr.append(square_error)

    return fitness_arr

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    start = time.time()
    with open('../../ga_log.txt', 'w') as f:
        f.write("")

    os.makedirs('../result', exist_ok=True)

    random.seed(64)
    
    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 100
    
    print("Start of evolution")
    fitnesses = eval_fractal(pop)

    write_log("pop", str(pop))
    write_log("fitnesses", str(fitnesses))
        
    for decimal_ind, fit in zip(pop, fitnesses):
        write_log("decimal_ind", str(decimal_ind))
        write_log("fit", str(fit))
        print("decimal_ind", decimal_ind)
        print("fit", fit)
        decimal_ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    with open('../ga_log.txt', 'a') as f:
            f.write("  Evaluated %i individuals\n" % len(pop))
    
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        with open('../ga_log.txt', 'a') as f:
            f.write("-- Generation %i --\n" % g)
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

            invalid_ind = [decimal_ind for decimal_ind in offspring if not decimal_ind.fitness.valid]
        fitnesses = eval_fractal(invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        with open('../ga_log.txt', 'a') as f:
            f.write("  Evaluated %i individuals\n" % len(invalid_ind))
        pop[:] = offspring
        
        fits = [decimal_ind.fitness.values[0] for decimal_ind in pop]
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
    
    print("-- End of (successful) evolution --")
    with open('../ga_log.txt', 'a') as f:
        f.write("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]

    num = str(best_ind[0])
    for i in range(1,var_num):
        num = num + str(best_ind[i])
    decimal_best_ind = int(num,2)
    decimal_best_ind = str(decimal_best_ind)

    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    with open('../ga_log.txt', 'a') as f:
            f.write("Best individual is %s, %s, %s\n" % (best_ind, decimal_best_ind, best_ind.fitness.values))
    
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == "__main__":
    main()