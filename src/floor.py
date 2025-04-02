import random
from collections import deque

class Floor:
    def __init__(self):
        # Randomly generate the floor matrix
        self.rows = random.randint(5, 10)
        self.cols = random.randint(5, 10)
        self.floorMatrix = [["." for _ in range(self.cols)] for _ in range(self.rows)]
            
    def createFloor(self):
        dirty_cells = random.randint(1, self.rows * self.cols // 2)
        walls = random.randint(1, self.rows * self.cols // 3)
        
        # Fill the floor with walls
        for _ in range(walls):
            row = random.randint(1, self.rows - 1)
            col = random.randint(1, self.cols - 1)
            self.floorMatrix[row][col] = "#"
        
        # Fill the floor with dirty cells
        for _ in range(dirty_cells):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.floorMatrix[row][col] = "D"
        
        # While it's not valid than create a new floor
        while not self.validateFloorPlan():
            self.createFloor()
        
    # Found some code online to validate the floor using BFS
    def validateFloorPlan(self):
        start_i, start_j = -1, -1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.floorMatrix[i][j] != "#":
                    start_i, start_j = i, j
                    break
            if start_i != -1:
                break
            
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        queue = deque([(start_i, start_j)])
        visited[start_i][start_j] = True
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            i, j = queue.popleft()
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                    if not visited[ni][nj] and self.floorMatrix[ni][nj] != "#":
                        visited[ni][nj] = True
                        queue.append((ni, nj))

        for i in range(self.rows):
            for j in range(self.cols):
                if self.floorMatrix[i][j] != "#" and not visited[i][j]:
                    return False
                
        return True
    
    #pretty print the floor
    def __str__(self):
        floor_str = ""
        for row in self.floorMatrix:
            floor_str += " ".join(row) + "\n"
        return floor_str