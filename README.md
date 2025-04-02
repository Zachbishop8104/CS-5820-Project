# Roomba Dungeon CSP Solver

## Overview

This project is a small Python application that generates a mxn dungeon where a Roomba (represented by the letter "R") must clean all the dirt in the dungeon while navigating around randomly generated walls. Unlike traditional coverage problems, the Roomba does not need to return to its starting position; the task is complete once every dirty cell is cleaned. The goal is to achieve this with the minimum number of moves possible.

## Project Description

The dungeon is represented as a grid where:
- **Walls** are denoted by `#` and block movement.
- **Open cells** are denoted by `.`.
- **Dirty cells** are denoted by `D`.
- The Roomba's starting position is at the top-left corner `(0, 0)` and is marked with an `A`.

The grid is generated randomly with configurable probabilities for walls and dirt. However, the generation process ensures:
1. No open cell is completely isolated.
2. All open cells are connected (i.e., every open cell is reachable from the start).

Once the dungeon is generated, an A* search algorithm is used to compute the optimal (least-cost) route that covers all open cells containing dirt, cleaning them along the way. After the route is computed, the solution is simulated, printing the dungeon state after each move to visually show the Roomba’s progress.

## How It Works

### Constraint Satisfaction Problem (CSP) Formulation

This project models the cleaning problem as a Constraint Satisfaction Problem (CSP) where:
- **Variables:** The dirty cells that must be cleaned.
- **Constraints:** Each cell that initially contains dirt must be visited and cleaned by the Roomba.

The state of the system is represented by a tuple consisting of:
- The current position of the Roomba.
- A set of cells where dirt has been cleaned.

The goal state is reached once all cells that started with dirt have been cleaned.

### Forward Checking and Constraint Propagation

- **Forward Checking:**  
  As the A* algorithm expands nodes (i.e., possible moves), it updates the state by marking cells as cleaned when the Roomba performs a cleaning action. This "forward" update immediately reflects the consequences of a move, thereby reducing the number of future moves (and states) to consider. Essentially, the solver is "checking forward" to see if cleaning a cell will help meet the constraints.

- **Constraint Propagation:**  
  In addition to forward checking, the algorithm prunes the search space by using memoization (branch-and-bound). For each state, if the solver has already reached a similar state (same current position and set of cleaned cells) with a lower cost, the current branch is pruned. This prevents unnecessary re-exploration of states that would not lead to an optimal solution.

### Heuristic Function

The A* algorithm uses a heuristic function to estimate the remaining cost (or number of moves) needed to reach the goal from the current state. The heuristic used here is:

```
h(state) = (number of remaining dirty cells) + (minimum Manhattan distance from current position to any remaining dirty cell)
```

- **Number of Remaining Dirty Cells:**  
  This term represents the minimum number of cleaning actions that must still be performed, since each dirty cell will need at least one cleaning action.

- **Minimum Manhattan Distance:**  
  This term provides a lower bound on the travel cost required to reach one of the remaining dirty cells. If there are no remaining dirty cells, the heuristic returns 0.

The heuristic is **admissible** because it never overestimates the true cost; it only provides a lower bound on the additional moves required. By combining these factors, the A* search is guided to explore promising states first and prunes less promising branches, thus efficiently searching for an optimal solution.

## Running the Project

1. **Requirements:**  
   The project is written in Python 3 and uses standard libraries such as `random`, `time`, `threading`, and `heapq`.

2. **Execution:**  
   When you run the script, it automatically generates the dungeon, computes the optimal cleaning route using A*, and then simulates the route by printing the dungeon state after each move with a short delay.

3. **Configuration:**  
   You can adjust parameters such as `GRID_SIZE`, `WALL_PROBABILITY`, and `DIRT_PROBABILITY` at the top of the code to experiment with different dungeon configurations.

## Conclusion

This project demonstrates how a complex coverage problem can be approached as a Constraint Satisfaction Problem (CSP) and solved using A* search with forward checking and constraint propagation. The combination of these techniques helps in effectively pruning the search space and guiding the search toward an optimal solution—minimizing the number of moves required for the Roomba to clean all dirt.

Enjoy exploring the code and feel free to experiment with the parameters and heuristic to further improve the solution!
