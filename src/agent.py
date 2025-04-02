from floor import Floor

class Agent:
    def __init__(self, name: str):
        self.name = name
        floor = Floor()
        floor.createFloor()
        self.floor = floor

    def __str__(self):
        return f"Agent({self.name})\n{self.floor}"