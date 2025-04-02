import sys
import random
import time
import threading
import heapq
from collections import deque

# --------------------------------------------------------------------------
# Configuration Parameters
# --------------------------------------------------------------------------
GRID_SIZE = random.randint(5, 10)                  # 4x4 grid
WALL_PROBABILITY = 0.3         # Chance that a cell is a wall
DIRT_PROBABILITY = 0.2         # Chance that an open cell (other than start) starts with dirt

# Possible movement directions
DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "east": (0, 1), "west": (0, -1)}

# --------------------------------------------------------------------------
# Cell Class
# Each cell can be open or a wall, and may have dirt.
# --------------------------------------------------------------------------
class Cell:
    def __init__(self):
        self.isWall = False
        self.hasDirt = False  # True if the cell originally contains dirt

# --------------------------------------------------------------------------
# GameState Class
# Generates the dungeon grid and ensures connectivity.
# --------------------------------------------------------------------------
class GameState:
    def __init__(self):
        # Create a GRID_SIZE x GRID_SIZE grid of Cells.
        self.grid = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # The Roomba always starts at (0,0)
        self.playerX = 0
        self.playerY = 0
        self.gameOver = False
        self.initialize_world()
    
    def initialize_world(self):
        # Randomly assign walls to cells (except the starting cell at (0,0)).
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) == (0, 0):
                    continue
                if random.random() < WALL_PROBABILITY:
                    self.grid[i][j].isWall = True
        
        # Ensure the starting cell is open.
        self.grid[0][0].isWall = False
        
        # Ensure that no open cell is isolated (each open cell has a neighbor).
        self.ensure_no_isolated_cells()
        
        # Ensure connectivity: every open cell must be reachable from (0,0).
        self.ensure_connectivity()
        
        # Randomly add dirt piles to open cells (except the starting cell).
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if not self.grid[i][j].isWall and (i, j) != (0, 0):
                    if random.random() < DIRT_PROBABILITY:
                        self.grid[i][j].hasDirt = True

    def ensure_no_isolated_cells(self):
        """
        For each open cell, if it has no adjacent open cell,
        force one neighboring cell to be open.
        """
        changed = True
        while changed:
            changed = False
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if not self.grid[i][j].isWall:
                        if not self.has_open_neighbor(i, j):
                            neighbors = self.get_neighbors(i, j)
                            if neighbors:
                                ni, nj = random.choice(neighbors)
                                if self.grid[ni][nj].isWall:
                                    self.grid[ni][nj].isWall = False
                                    changed = True

    def has_open_neighbor(self, i, j):
        """Return True if cell (i,j) has at least one adjacent open cell."""
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = i+dx, j+dy
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                if not self.grid[ni][nj].isWall:
                    return True
        return False

    def get_neighbors(self, i, j):
        """Return a list of valid neighboring cell coordinates (4-neighborhood)."""
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = i+dx, j+dy
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                neighbors.append((ni, nj))
        return neighbors

    def flood_fill(self, start):
        """
        Perform flood fill from 'start' and return the set of open cells reached.
        This is used to ensure connectivity.
        """
        reached = set()
        queue = deque([start])
        while queue:
            cell = queue.popleft()
            if cell in reached:
                continue
            reached.add(cell)
            i, j = cell
            for ni, nj in self.get_neighbors(i, j):
                if not self.grid[ni][nj].isWall and (ni, nj) not in reached:
                    queue.append((ni, nj))
        return reached

    
    def ensure_connectivity(self):
        """
        Note: I used an LLM for this ensure_connectivity. I had no idea how to do this section 
        and quite frankly couldn't be bothered to learn how to in my 3am red bull fueled coding session. 
        But it works and thats good enough for me.
        
        Ensure that every open cell is reachable from (0,0).
        If not, remove a wall along the boundary between disconnected regions.
        """
        main_region = self.flood_fill((0, 0))
        all_open = {(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                    if not self.grid[i][j].isWall}
        while all_open - main_region:
            target = (all_open - main_region).pop()
            target_region = self.flood_fill(target)
            connected = False
            for i, j in target_region:
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i+dx, j+dy
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                        if self.grid[ni][nj].isWall:
                            # Remove wall if it connects to the main region.
                            for ddx, ddy in [(-1,0), (1,0), (0,-1), (0,1)]:
                                wi, wj = ni+ddx, nj+ddy
                                if 0 <= wi < GRID_SIZE and 0 <= wj < GRID_SIZE:
                                    if (wi, wj) in main_region:
                                        self.grid[ni][nj].isWall = False
                                        connected = True
                                        break
                            if connected:
                                break
                if connected:
                    break
            main_region = self.flood_fill((0, 0))
            all_open = {(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                        if not self.grid[i][j].isWall}

# --------------------------------------------------------------------------
# Function to Print the Dungeon
# "A" marks the Roomba, "#" marks walls, "D" marks dirt, and "." marks open cells.
# --------------------------------------------------------------------------
def print_world(game):
    print("\nDungeon:")
    header = "    " + "  ".join(str(j) for j in range(GRID_SIZE))
    print(header)
    print("   " + "---"*GRID_SIZE)
    for i in range(GRID_SIZE):
        row_str = f"{i} | "
        for j in range(GRID_SIZE):
            symbol = "."
            if game.playerX == i and game.playerY == j:
                symbol = "A"
            else:
                cell = game.grid[i][j]
                if cell.isWall:
                    symbol = "#"
                elif cell.hasDirt:
                    symbol = "D"
            row_str += symbol + "  "
        print(row_str)
    print()

# --------------------------------------------------------------------------
# A* Solver: Clean All Dirt with Minimum Moves
#
# We model the problem as a CSP:
#   - Variables: The dirt cells that need cleaning.
#   - Constraints: Each dirt cell must be cleaned by the Roomba.
#
# State Representation: (current_position, frozenset(cleaned))
#   - current_position: The Roomba's current coordinates.
#   - cleaned: Set of coordinates for dirt cells that have been cleaned.
#
# Actions:
#   - "move": Move to a neighboring cell (cost = 1).
#   - "clean": Clean the current cell if it originally had dirt (cost = 1).
#
# The goal is reached when all dirt cells (from the initial grid) have been cleaned.
#
# Heuristic:
#   h(state) = (number of remaining dirt cells) + (minimum Manhattan distance from current position to any remaining dirty cell)
# If there are no remaining dirt cells, h(state) = 0.
# --------------------------------------------------------------------------
def manhattan_distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def solve_cleaning_A_star(game):
    # Build set of open cells and set of dirt cells from the initial grid.
    open_cells = {(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                  if not game.grid[i][j].isWall}
    dirt_set = {(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                if not game.grid[i][j].isWall and game.grid[i][j].hasDirt}
    start = (0, 0)
    total_dirt = len(dirt_set)
    
    # Our state now is just (current_position, frozenset(cleaned))
    start_state = (start, frozenset())
    g_start = 0

    # Heuristic: If there are remaining dirt cells, use:
    #   (number of remaining dirt cells) + (min distance from current to any remaining dirt)
    # Otherwise, heuristic = 0.
    def heuristic(state):
        current, cleaned = state
        remaining = dirt_set - set(cleaned)
        if not remaining:
            return 0
        min_dist = min(manhattan_distance(current, d) for d in remaining)
        return len(remaining) + min_dist

    f_start = g_start + heuristic(start_state)
    # Priority queue elements: (f, g, state, path)
    pq = [(f_start, g_start, start_state, [("move", start)])]
    
    memo = {}  # To store best cost for a given state.
    best_solution = None
    best_cost = float('inf')
    
    while pq:
        f, g, state, path = heapq.heappop(pq)
        current, cleaned = state
        
        # Goal: all dirt cells have been cleaned.
        if len(cleaned) == total_dirt:
            if g < best_cost:
                best_cost = g
                best_solution = path
                break
        
        if state in memo and memo[state] <= g:
            continue
        memo[state] = g
        
        # Option: Clean at current cell if it is dirty and not yet cleaned.
        if current in dirt_set and current not in cleaned:
            new_state = (current, frozenset(set(cleaned) | {current}))
            new_g = g + 1
            new_f = new_g + heuristic(new_state)
            heapq.heappush(pq, (new_f, new_g, new_state, path + [("clean", current)]))
        
        # Expand moves: try moving in each of the four directions.
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if neighbor in open_cells:
                    new_state = (neighbor, cleaned)
                    new_g = g + 1
                    new_f = new_g + heuristic(new_state)
                    heapq.heappush(pq, (new_f, new_g, new_state, path + [("move", neighbor)]))
    
    return best_solution, best_cost

# --------------------------------------------------------------------------
# Simulation Function
# This function simulates the route by updating the game state and printing the board after each action.
# --------------------------------------------------------------------------
def simulate_route(game, route):
    # Create a copy of the game state for simulation.
    sim_game = GameState()
    # Copy the grid data from the original game.
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            sim_game.grid[i][j].isWall = game.grid[i][j].isWall
            sim_game.grid[i][j].hasDirt = game.grid[i][j].hasDirt
    # Roomba starts at (0,0)
    sim_game.playerX, sim_game.playerY = 0, 0
    
    print("\nSimulating route:")
    print_world(sim_game)
    time.sleep(1)
    
    # Execute each action in the route.
    for action in route[1:]:  # The route already starts with ("move", (0,0))
        act, pos = action
        if act == "move":
            sim_game.playerX, sim_game.playerY = pos
            print(f"\nAction: Move to {pos}")
        elif act == "clean":
            # Clean the current cell.
            sim_game.grid[sim_game.playerX][sim_game.playerY].hasDirt = False
            print(f"\nAction: Clean dirt at {pos}")
        print_world(sim_game)
        time.sleep(0.5)

# --------------------------------------------------------------------------
# Solver Runner
# This function runs the A* solver in a separate thread while displaying elapsed time,
# then simulates the found route.
# --------------------------------------------------------------------------
def solve_and_show(game):
    print("Finding the optimal route to clean all dirt (minimizing moves)...")
    result_container = {}
    
    def worker():
        sol, cost = solve_cleaning_A_star(game)
        result_container["solution"] = sol
        result_container["cost"] = cost
    
    solver_thread = threading.Thread(target=worker)
    solver_thread.start()
    
    start_time = time.time()
    while solver_thread.is_alive():
        elapsed = time.time() - start_time
        print(f"Time elapsed: {elapsed:.1f} seconds", end="\r")
        time.sleep(0.5)
    solver_thread.join()
    print()
    
    solution = result_container.get("solution", None)
    cost = result_container.get("cost", None)
    if solution:
        print(f"\nFound a route of cost {cost}:")
        for action in solution:
            if action[0] == "move":
                print(f"Move to {action[1]}")
            elif action[0] == "clean":
                print(f"Clean dirt at {action[1]}")
        simulate_route(game, solution)
    else:
        print("\nNo route to clean all dirt was found.")

# --------------------------------------------------------------------------
# Main Function
# Generates the game state, prints the board, and runs the solver.
# --------------------------------------------------------------------------
def main():
    game = GameState()
    print_world(game)
    solve_and_show(game)

if __name__ == "__main__":
    main()
