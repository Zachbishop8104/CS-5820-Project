import random
from collections import deque

class Floor:
    """
    Represents the dungeon grid.

    The grid consists of:
    - Walls (#): impassable by the agent
    - Dirt (D): must be cleaned
    - Open spaces (.): traversable
    - Agent (A): starts at (0, 0)

    This class generates a valid, connected dungeon
    with randomized walls and dirt.
    """

    def __init__(self):
        self.rows = 4
        self.cols = 4
        self.floorMatrix = [["." for _ in range(self.cols)] for _ in range(self.rows)]

    def createFloor(self):
        """
        Randomly populates the grid with walls and dirt, then validates it.
        Walls and dirt are not placed on the starting cell (0,0).
        """
        walls = random.randint(1, 4)
        dirt = random.randint(2, 5)

        # Place walls randomly
        for _ in range(walls):
            i, j = random.randint(0, 3), random.randint(0, 3)
            if (i, j) != (0, 0):
                self.floorMatrix[i][j] = "#"

        # Place dirt on open cells
        for _ in range(dirt):
            i, j = random.randint(0, 3), random.randint(0, 3)
            if self.floorMatrix[i][j] == "." and (i, j) != (0, 0):
                self.floorMatrix[i][j] = "D"

        # Ensure the map is connected and solvable
        while not self.validateFloorPlan():
            self.__init__()
            self.createFloor()

    def validateFloorPlan(self):
        """
        Validates that all open cells are reachable from the start (0, 0).
        Uses BFS to enforce a single connected region (constraint propagation).
        """
        start = (0, 0)
        if self.floorMatrix[0][0] == "#":
            return False

        visited = [[False] * self.cols for _ in range(self.rows)]
        queue = deque([start])
        visited[0][0] = True
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            i, j = queue.popleft()
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                    if self.floorMatrix[ni][nj] != "#" and not visited[ni][nj]:
                        visited[ni][nj] = True
                        queue.append((ni, nj))

        # Ensure all non-wall cells are visited
        for i in range(self.rows):
            for j in range(self.cols):
                if self.floorMatrix[i][j] != "#" and not visited[i][j]:
                    return False
        return True

    def clone(self):
        """Creates a copy of the current floor layout for simulation purposes."""
        new_floor = Floor()
        new_floor.floorMatrix = [row[:] for row in self.floorMatrix]
        return new_floor

    def __str__(self):
        """Returns a string rendering of the dungeon for console output."""
        return "\n".join(" ".join(row) for row in self.floorMatrix) + "\n"
