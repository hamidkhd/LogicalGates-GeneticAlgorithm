import numpy as np 
import random
import csv 
import time

gates = ['and', 'or', 'xor', 'nand', 'nor', 'xnor']

class Chromosome:
    def __init__(self):
        self.gates = list()
        self.fitness = int(0)

    def fitness_calculation(self, input_data):
        value = int()
        for i in range(1, len(input_data)):
            for j in range(1, len(input_data[i])):
                if j == 1:
                    value = self.gates_value_table(input_data[i][j-1], input_data[i][j], self.gates[j-1])
                elif j != len(input_data[i])-1:
                    value = self.gates_value_table(value, input_data[i][j], self.gates[j-1])
                else:
                    if input_data[i][j] == value:
                        self.fitness += 1

    def gates_value_table(self, a, b, type):
        if type == "and":
            return "TRUE" if a == b == "TRUE" else "FALSE"

        elif type == "or":
            return "FALSE" if a == b == "FALSE" else "TRUE"

        elif type == "xor":
            return "FALSE" if a == b == "FALSE" or a == b == "TRUE" else "TRUE"

        elif type == "nand":
            return "FALSE" if a == b == "TRUE" else "TRUE"

        elif type == "nor":
            return "TRUE" if a == b == "FALSE" else "FALSE"

        elif type == "xnor":
            return "TRUE" if a == b == "FALSE" or a == b == "TRUE" else "FALSE"

def population_building(input_data):
    population = list()
    temp_gates = list()

    value = 2 ** (len(input_data[0])-3)

    for i in range(value):
        x = np.random.choice(gates, size=len(input_data[0])-2, replace=True)
        for x in x:
            temp_gates.append(x)

        new_chromosome = Chromosome()
        new_chromosome.gates = temp_gates.copy()
        new_chromosome.fitness_calculation(input_data)
        population.append(new_chromosome)
        temp_gates.clear()

    return population 

def selection(population, input_data):
    population = sorted(population, key=lambda x: x.fitness) 
    fitness_rank = [i ** 2 for i in range(len(population))]
    population = random.choices(population, weights= fitness_rank, k=len(population))
    return population

def crossover(population, input_data):
    new_population = list()
    p_c = sum([i.fitness for i in population]) / len(population)

    for i in range(len(population)//2):
        rand_people = np.random.choice(population, size=2, replace=False)
        parent_a, parent_b = rand_people

        p_rand = random.randint(0, len(input_data)-1)

        if p_rand < p_c:
            child1, child2 = crossover_helper(parent_a, parent_b, input_data)
            new_population.append(child1)
            new_population.append(child2)
        else:
            new_population.append(parent_a)
            new_population.append(parent_b)

    return new_population

def crossover_helper(parent_a, parent_b, input_data):
    a = parent_a.gates
    b = parent_b.gates
    point = random.randint(0, len(input_data[0])-1)

    new_a = Chromosome()
    new_a.gates = a[:point]+b[point:]
    new_a.fitness_calculation(input_data)

    new_b = Chromosome()
    new_b.gates = b[:point]+a[point:]
    new_b.fitness_calculation(input_data)

    return new_a, new_b

def mutation(population, input_data, weight):
    p_m = (1 / len(population[0].gates)) * weight

    for i in population:
        new_gates = list()

        for j in i.gates:
            p_rand = random.random()

            if p_rand < p_m:
                new_gates.append(np.random.choice(gates, size=1, replace=True)[0])
            else:
                new_gates.append(j)

        i.gates = new_gates
        i.fitness = 0
        i.fitness_calculation(input_data)

    return population

def get_file_data(file_name):
    table_info = list()

    with open(file_name, mode = 'r') as file:     
        csv_file = csv.reader(file)  
        for line in csv_file:    
            table_info.append(line) 
    
    return table_info

def main():
    input_data = get_file_data("truth_table.csv")
    population = population_building(input_data)

    counter = int(0)
    repeat = int(0)
    pre_result = int(0)
    weight = int(1)

    start = time.process_time()
    while True:
        population = selection(population, input_data)
        population = crossover(population, input_data)
        population = mutation(population, input_data, weight)

        result = max([i.fitness for i in population])

        repeat += 1 if pre_result == result else 0

        if repeat >= 2:
            flag = 4
            repeat = 0
        else:
            flag = 1

        pre_result = result
        counter += 1        
        
        end = time.process_time()
        print(counter, result, end-start, "s")
        
        if result == len(input_data)-1:
            for i in population:
                if i.fitness == len(input_data)-1:
                    print(i.gates)
            break

if __name__ == "__main__":
    main()