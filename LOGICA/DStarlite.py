import heapq
import math
import numpy as np
import random


def add_random_obstacles(grid, prob, start, goal):
    size_x, size_y = grid.shape
    for x in range(size_x):
        for y in range(size_y):
            if (x, y) != start and (x, y) != goal:
                if random.random() < prob:
                    grid[x][y] = 1
                else:
                    grid[x][y] = 0
    return grid


def move_obstacles(grid, prob, start, goal):
    size_x, size_y = grid.shape
    obstacles = [(x, y) for x in range(size_x) for y in range(size_y) if grid[x][y] == 1]

    for x, y in obstacles:
        if random.random() < prob:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size_x and 0 <= ny < size_y:
                    if grid[nx][ny] == 0 and (nx, ny) != start and (nx, ny) != goal:
                        grid[nx][ny] = 1
                        grid[x][y] = 0
                        break
    return grid


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}  # nodo -> (k1, k2, nodo)

    def insert(self, node, priority):
        entry = (priority[0], priority[1], node)
        self.entry_finder[node] = entry
        heapq.heappush(self.heap, entry)

    def update(self, node, priority):
        self.remove(node)
        self.insert(node, priority)

    def remove(self, node):
        if node in self.entry_finder:
            entry = self.entry_finder.pop(node)
            self.heap.remove(entry)
            heapq.heapify(self.heap)

    def pop(self):
        while self.heap:
            k1, k2, node = heapq.heappop(self.heap)
            if node in self.entry_finder and self.entry_finder[node] == (k1, k2, node):
                self.entry_finder.pop(node)
                return node
        return None

    def top(self):
        while self.heap:
            k1, k2, node = self.heap[0]
            if node in self.entry_finder:
                return node
            else:
                heapq.heappop(self.heap)
        return None

    def top_key(self):
        while self.heap:
            k1, k2, node = self.heap[0]
            if node in self.entry_finder:
                return (k1, k2)
            else:
                heapq.heappop(self.heap)
        return (math.inf, math.inf)

    def contains(self, node):
        return node in self.entry_finder

    def empty(self):
        return len(self.entry_finder) == 0


class DStarLite:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.k_m = 0
        self.s_last = start

        self.g = {}
        self.rhs = {}

        self.U = PriorityQueue()

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                self.g[(x, y)] = math.inf
                self.rhs[(x, y)] = math.inf

        self.rhs[goal] = 0
        self.U.insert(goal, self.calculate_key(goal))

    def calculate_key(self, s):
        val = min(self.g[s], self.rhs[s])
        return (val + manhattan(self.start, s) + self.k_m, val)

    def neighbors(self, s):
        x, y = s
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        result = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                if self.grid[nx][ny] == 0:  # libre
                    result.append((nx, ny))
        return result

    def cost(self, u, v):
        if self.grid[v[0]][v[1]] == 1:  # obstáculo
            return math.inf
        return 1  # coste uniforme

    def update_vertex(self, u):
        if u != self.goal:
            self.rhs[u] = min([self.cost(u, s) + self.g[s] for s in self.neighbors(u)] or [math.inf])
        if self.U.contains(u):
            self.U.remove(u)
        if self.g[u] != self.rhs[u]:
            self.U.insert(u, self.calculate_key(u))

    def compute_shortest_path(self):
        while (self.U.top_key() < self.calculate_key(self.start)) or (self.rhs[self.start] != self.g[self.start]):
            u = self.U.top()
            k_old = self.U.top_key()
            k_new = self.calculate_key(u)

            if k_old < k_new:
                self.U.update(u, k_new)
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                self.U.remove(u)
                for s in self.neighbors(u):
                    self.update_vertex(s)
            else:
                g_old = self.g[u]
                self.g[u] = math.inf
                for s in self.neighbors(u) + [u]:
                    if self.rhs[s] == self.cost(s, u) + g_old:
                        if s != self.goal:
                            self.rhs[s] = min([self.cost(s, sp) + self.g[sp] for sp in self.neighbors(s)] or [math.inf])
                    self.update_vertex(s)

    def plan(self):
        self.compute_shortest_path()
        if self.g[self.start] == math.inf:
            return None

        path = [self.start]
        s = self.start
        while s != self.goal:
            min_cost = math.inf
            next_s = None
            for sp in self.neighbors(s):
                val = self.cost(s, sp) + self.g[sp]
                if val < min_cost:
                    min_cost = val
                    next_s = sp
            if next_s is None:
                return None
            s = next_s
            path.append(s)
        return path


def run_DStarlite(size):
    while True:
        grid = np.zeros((size, size), dtype=int)
        start = (int(size/2),int(size/2))
        goal = (random.randint(0, size - 1), random.randint(0, size - 1))

        grids = []  # lista de tableros
        jugadas = []
        while goal == start:
            goal = (random.randint(0, size - 1), random.randint(0, size - 1))
        current_start = start

        grid = add_random_obstacles(grid, prob=map_value(size), start=current_start, goal=goal)
        grids.append(np.copy(grid))

        dstar = DStarLite(grid, current_start, goal)
        path = dstar.plan()
        caminos = []
        if path is not None:
            for step in path[1:]:
                current_start = step
                jugadas.append(step)

                grid = move_obstacles(grid, prob=0.2, start=current_start, goal=goal)
                grids.append(np.copy(grid))
                dstar = DStarLite(grid, current_start, goal)
                new_path = dstar.plan()
                if new_path is None:
                    break
                else:
                    path = new_path

            if current_start == goal:
                break
            pass

        else:
            pass

    return (start, goal, jugadas, grids)

def map_value(x):
    x1, x2 = 5, 50
    y1, y2 = 0.5, 0.05
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
