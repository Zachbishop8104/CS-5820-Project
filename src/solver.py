import heapq

def solve_cleaning_a_star(start, floorMatrix, dirt_set):
    """
    Solves the cleaning problem using A* search with forward checking.

    Goal: Clean all dirty cells using the minimum number of moves.

    CSP Model:
    - Variables: All cells that initially contain dirt
    - Domain: Possible sequences of moves leading to each dirt cell
    - Constraints:
        1. All dirt cells must be visited and cleaned
        2. The agent may only move to valid (non-wall) neighbors

    A* with forward checking:
    - The agent tracks what dirt has been cleaned
    - Memoization prevents revisiting the same state with a higher cost
    - Heuristic guides search based on proximity to remaining dirt
    """

    rows, cols = len(floorMatrix), len(floorMatrix[0])
    total_dirt = len(dirt_set)
    start_state = (start, frozenset())  # current position, cleaned dirt set
    g_start = 0  # cost so far

    # Heuristic: 
    # Estimate remaining cost by:
    # - Number of dirt cells left to clean
    # - Minimum Manhattan distance to the nearest dirty cell
    def heuristic(state):
        current, cleaned = state
        remaining = dirt_set - set(cleaned)
        if not remaining:
            return 0
        min_dist = min(abs(current[0]-d[0]) + abs(current[1]-d[1]) for d in remaining)
        return len(remaining) + min_dist

    f_start = g_start + heuristic(start_state)
    pq = [(f_start, g_start, start_state, [("move", start)])]
    memo = {}  # used for forward checking (pruning)

    while pq:
        f, g, state, path = heapq.heappop(pq)
        current, cleaned = state

        # Check if goal state (all dirt cleaned)
        if len(cleaned) == total_dirt:
            return path, g

        # Constraint propagation: prune if visited with lower cost
        if state in memo and memo[state] <= g:
            continue
        memo[state] = g

        # Cleaning action (cost = 1)
        if current in dirt_set and current not in cleaned:
            new_cleaned = frozenset(set(cleaned) | {current})
            heapq.heappush(pq, (
                g + 1 + heuristic((current, new_cleaned)),
                g + 1,
                (current, new_cleaned),
                path + [("clean", current)]
            ))

        # Movement actions (cardinal directions)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and floorMatrix[nx][ny] != "#":
                heapq.heappush(pq, (
                    g + 1 + heuristic(((nx, ny), cleaned)),
                    g + 1,
                    ((nx, ny), cleaned),
                    path + [("move", (nx, ny))]
                ))

    return None, float("inf")
