import random

#making random chromosomes
def Make_Random_chorm(size):  
    return [ random.randint(1, n_queen) for _ in range(n_queen) ]

# calculate Fitness_Value with fitness function 
def Fitness_Value(chromosome):
    horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(Fmax - (horizontal_collisions + diagonal_collisions)) #28-(2+3)=23

# calculate probability of chorm in population
def probability(chromosome, fitness):
    return fitness(chromosome) / Fmax

# select a best point in population 
def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

#doing cross_over between two selected chromosomes  
def reproduce(x, y): 
    l = len(x)
    mid_point = random.randint(0, l - 1)
    return x[0:mid_point] + y[mid_point:l]

#randomly changing the value of a random index of a chromosome
def mutate(x):  
    l = len(x)
    Random_index = random.randint(0, l - 1)
    New_random_gene = random.randint(1, l)
    x[Random_index] = New_random_gene
    return x

#Genetic_Algo step by step :
# 1- Select two best Chorom for Cross_over([a,b|,c,d,e] + [f,g|,h,i,j] = [a,b|,h,i,j]).
# 2- If need to mutation mutate(kept mutation low).
# 3- Add new chorom to population.
def genetic_queen(population, Fitness_Value):
    mutation_probability = 0.03
    new_population = []
    probabilities = [probability(n, Fitness_Value) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child)
        new_population.append(child)
        if Fitness_Value(child) == Fmax: break
    return new_population

def print_chromosome(chrom):
    print("Chromosome = {},  Fitness_Value = {}"
        .format(str(chrom), Fitness_Value(chrom)))

if __name__ == "__main__":
    n_queen = int(input("Enter Number of Queens: ")) #say N = 100
    Fmax = (n_queen*(n_queen-1))/2  # 100*99/2 = 
    population = [Make_Random_chorm(n_queen) for _ in range(100)]
    generation = 1
    while not Fmax in [Fitness_Value(chrom) for chrom in population]:
        print("--- Generation {} ---".format(generation))
        population = genetic_queen(population, Fitness_Value)
        print("")
        print("Maximum Fitness = {}".format(max([Fitness_Value(n) for n in population])))
        generation += 1
    chrom_out = []
    print("Solved in Generation {}!".format(generation-1))
    for chrom in population:
        if Fitness_Value(chrom) == Fmax:
            print("");
            print("One of the solutions: ")
            chrom_out = chrom
            print_chromosome(chrom)

    #make board      
    board = []
    for x in range(n_queen):
        board.append(["x"] * n_queen)   
    for i in range(n_queen):
        board[n_queen-chrom_out[i]][i]="Q"
    def print_board(board):
        for row in board:
            print (" ".join(row))       
    print()
    print_board(board)