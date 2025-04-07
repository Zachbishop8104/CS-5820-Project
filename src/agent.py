import time
from floor import Floor
from solver import solve_cleaning_a_star

class Agent:
    """
    Represents the Roomba agent.

    - Initializes the environment
    - Solves the cleaning problem using A*
    - Simulates the computed route step-by-step
    """

    def __init__(self, name: str):
        self.name = name
        self.floor = Floor()
        self.floor.createFloor()
        self.floor.floorMatrix[0][0] = "A"  # place the agent at start

    def __str__(self):
        return f"Agent({self.name})\n{self.floor}"

    def getDirtCells(self):
        """Returns coordinates of all dirty cells in the dungeon."""
        dirt = set()
        for i in range(self.floor.rows):
            for j in range(self.floor.cols):
                if self.floor.floorMatrix[i][j] == "D":
                    dirt.add((i, j))
        return dirt

    def simulateRoute(self, route):
        """
        Simulates each action in the computed route:
        - Moves the agent
        - Cleans dirt
        - Updates and prints the dungeon after each step
        """
        sim_floor = self.floor.clone()
        agent_pos = (0, 0)
        print("\nSimulating route:")
        print(sim_floor)
        time.sleep(1)

        for action, pos in route[1:]:
            if action == "move":
                r, c = agent_pos
                if sim_floor.floorMatrix[r][c] != "D":
                    sim_floor.floorMatrix[r][c] = "."
                agent_pos = pos
                sim_floor.floorMatrix[pos[0]][pos[1]] = "A"
                print(f"\nAction: Move to {pos}")
            elif action == "clean":
                print(f"\nAction: Clean dirt at {pos}")
                sim_floor.floorMatrix[pos[0]][pos[1]] = "A"
            print(sim_floor)
            time.sleep(0.5)

    def run(self):
        """Executes the full clean-and-simulate process."""
        dirt_set = self.getDirtCells()
        solution, cost = solve_cleaning_a_star(
            start=(0, 0),
            floorMatrix=self.floor.floorMatrix,
            dirt_set=dirt_set
        )
        if solution:
            print(f"\nFound a route of cost {cost}:")
            for action in solution:
                print(f"{action[0].capitalize()} to {action[1]}")
            self.simulateRoute(solution)
        else:
            print("No route found to clean all dirt.")
