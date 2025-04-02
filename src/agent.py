from floor import Floor

class Agent:
    def __init__(self, name: str):
        self.name = name
        floor = Floor()
        floor.createFloor()
        
        floor.floorMatrix[0][0] = "A" # Agent starts at (0, 0)
        
        self.floor = floor

    def __str__(self):
        return f"Agent({self.name})\n{self.floor}"