import random
import numpy as np
from constants import CellType

def add_random_obstacles(grid, prob, start, goal, fake):
    size_x, size_y = grid.shape
    for x in range(size_x):
        for y in range(size_y):
            if (x, y) != start and (x, y) != goal and (x,y) not in fake:
                if random.random() < prob:
                    grid[x][y] = 1
                else:
                    grid[x][y] = 0
    return grid

def add_fake_goals(grid, exit_count, start, goal):
    size_x, size_y = grid.shape
    fake_goals = []
    for _ in range(exit_count - 1):
        fake_pos = [random.randint(0, size_x - 1), random.randint(0, size_y - 1)]
        while fake_pos == start or fake_pos == goal or fake_pos in fake_goals:
            pos_salida = [random.randint(0, size_x - 1), random.randint(0, size_y - 1)]
        fake_goals.append(fake_pos)
    return fake_goals

def map_value(x):
    x1, x2 = 10, 50
    y1, y2 = 0.4, 0.05
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

# mapping: 0=Arriba,1=Derecha,2=Abajo,3=Izquierda
MOVES = {
    0: (-1, 0), #Mover hacia arriba
    1: (0, 1),  #Mover hacia la derecha
    2: (1, 0),  #Mover hacia abajo
    3: (0, -1)  #Mover hacia la izquierda
}

class GeneticAlgorithm:
    def __init__(self, size, population_size, num_generations, chromosome_length, mutation_rate, crossover_rate):
        # Tablero
        self.size_board = size
        self.board = np.zeros((self.size_board, self.size_board), dtype=int)
        self.start = (0,0)
        self.goal = (random.randint(9, size - 1), random.randint(9, size - 1))
        self.boards = []

        while self.goal == self.start:
            self.goal = (random.randint(0, size - 1), random.randint(0, size - 1))

        self.fake_goals = add_fake_goals(self.board, 2, self.start, self.goal)
        self.board = add_random_obstacles(self.board, map_value(self.size_board), self.start, self.goal, self.fake_goals)
        self.boards.append(self.board)

        self.population_size = population_size
        self.num_generations = num_generations
        self.chromosome_length = chromosome_length
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = self.generate_initial_population()

    def generate_initial_population(self):
        population = []
        for i in range(self.population_size):
            chromosome = []
            for _ in range (self.chromosome_length):
                value = random.randint(0,3)
                # Mover hacia arriba
                if value == 0:
                    chromosome.append((-1, 0))
                # Mover hacia derecha
                elif value == 1:
                    chromosome.append((0, 1))
                # Mover hacia abajo
                elif value == 2:
                    chromosome.append((1, 0))
                # Mover hacia izquierda
                elif value == 3:
                    chromosome.append((0, -1))
            population.append(chromosome)
        return population

    def simulate_chromosome(self, chromosome):
        (x, y) = self.start
        path = [(x, y)]
        penalties = 0
        steps = 0
        reached = False
        i=0

        for gene in chromosome:
            board = self.boards[i]
            x_mov, y_mov = gene
            new_x, new_y = x + x_mov, y + y_mov

            if not (0 <= new_x < self.size_board  and 0 <= new_y < self.size_board):
                penalties += 1
                path.append((x, y))
            else:
                cell = board[new_x][new_y]
                if cell == CellType.MURO:
                    penalties += 1
                    path.append((x,y))
                else:
                    x, y = new_x, new_y
                    path.append((x,y))
                    if (x,y) == self.goal:
                        reached = True
                        steps+=1
                        break
                    elif (x,y) == self.fake_goals:
                        penalties += 2
            steps+=1
            i+=1

        return (x,y), path, penalties, steps, reached

    def fitness_func(self, chromosome):
        (x,y), path, penalties, steps, reached = self.simulate_chromosome(chromosome)
        # Distancia Manhattan
        x_final, y_final = self.goal
        dist = abs(x - x_final) + abs (y - y_final)

        base_score = 1000
        score = base_score - (dist * 10) - (penalties * 20) - steps

        if reached:
            score += 10000 - (steps - 50)

        if score < 1:
            score = 1

        return score, reached

    def select_parent(self, fitness_population):
        total = sum(fitness_population)
        if total == 0:
            return random.choice(self.population)
        # pick determina donde cae la aguja en la ruleta, cada cormosoma tiene probabilidad proporcional a su fitness (los cromosomas buenos tienen mas probabilidad)
        pick = random.uniform(0, total) # numero aleatorio entre 0 y la suma de todos los fitnesses
        current = 0
        for i in range(self.population_size):
            chromosome = self.population[i]
            fitness = fitness_population[i]

            current += fitness
            if current > pick:
                return chromosome

        return self.population[-1]

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            # Se elige un punto de corte aleatorio
            idx = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:idx] + parent2[idx:]
            child2 = parent2[:idx] + parent1[idx:]
        else:
            # Caso que la probabilidad falla se copian tal cual
            return parent1[:], parent2[:]

        return child1, child2

    def mutate(self, chromosome):
        c = chromosome[:]
        for i in range(self.chromosome_length):
            if random.random() < self.mutation_rate:
                value = random.randint(0,3)
                # Mover hacia arriba
                if value == 0:
                    chromosome.append((-1, 0))
                # Mover hacia derecha
                elif value == 1:
                    chromosome.append((0, 1))
                # Mover hacia abajo
                elif value == 2:
                    chromosome.append((1, 0))
                # Mover hacia izquierda
                elif value == 3:
                    chromosome.append((0, -1))
        return c

    def run(self):
        # Tablero
        best_fit = -float('inf')
        best_chromosome = None
        reached_population = []
        fitness_population = []

        for i in range(self.num_generations):
            # Calcular fitness de cada cromosoma, guardar si llego a la meta o no
            for chromosome in self.population:
                score, reached= self.fitness_func(chromosome)
                fitness_population.append(score)
                reached_population.append(reached)

            # Revisar si algun cromosoma llegó a la meta, quedarnos con el mejor camino cada vez
            for i in range(self.population_size):
                chromosome = self.population[i]
                fitness = fitness_population[i]
                (x,y), path, penalties, steps, reached = self.simulate_chromosome(chromosome)
                if reached:
                    best_fit = fitness
                    best_chromosome = chromosome[:] # guardamos una copia, chromosome original puede variar
                    best_path = path[:]
                    return (self.start, self.goal, best_path, self.boards)

                elif fitness>best_fit:
                    best_fit = fitness
                    best_chromosome = chromosome[:]
                    best_path = path[:]


            new_population = []
            while len(new_population) < self.population_size:
                parent1 = self.select_parent(fitness_population)
                parent2 = self.select_parent(fitness_population)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)


        return (self.start, self.goal, best_path, self.boards)