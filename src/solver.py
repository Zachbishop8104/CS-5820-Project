import heapq

def solve_cleaning_a_star(start, floorMatrix, dirt_set):
    """
    A* Solver that finds the minimum number of moves to:
    1. Clean all dirt cells
    2. Return to the starting position (0,0)

    This is a CSP:
    - Variables: dirt cells
    - Constraints: all dirt must be cleaned AND the final position must be the start
    - State: (agent_position, cleaned_dirt_set)

    Implements forward checking and constraint propagation by:
    - Memoizing visited states with cost (branch & bound)
    - Heuristic: estimated cost to complete cleaning + return to start
    """

    rows, cols = len(floorMatrix), len(floorMatrix[0])
    total_dirt = len(dirt_set)
    start_state = (start, frozenset())  # (position, cleaned dirt set)
    g_start = 0

    def heuristic(state):
        """
        Heuristic estimates:
        - Remaining cleaning steps
        - Distance to nearest dirty cell (if any remain)
        - If all clean, distance to return to start
        """
        current, cleaned = state
        remaining = dirt_set - set(cleaned)

        if not remaining:
            # All cleaned: estimate return to start
            return abs(current[0] - start[0]) + abs(current[1] - start[1])

        min_dist = min(abs(current[0] - d[0]) + abs(current[1] - d[1]) for d in remaining)
        return len(remaining) + min_dist

    f_start = g_start + heuristic(start_state)
    pq = [(f_start, g_start, start_state, [("move", start)])]
    memo = {}
    best_solution = None
    best_cost = float("inf")

    while pq:
        f, g, state, path = heapq.heappop(pq)
        current, cleaned = state

        # GOAL: All dirt cleaned AND returned to start
        if len(cleaned) == total_dirt and current == start:
            return path, g

        if state in memo and memo[state] <= g:
            continue
        memo[state] = g

        # Clean action
        if current in dirt_set and current not in cleaned:
            new_cleaned = frozenset(set(cleaned) | {current})
            heapq.heappush(pq, (
                g + 1 + heuristic((current, new_cleaned)),
                g + 1,
                (current, new_cleaned),
                path + [("clean", current)]
            ))

        # Move action
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and floorMatrix[nx][ny] != "#":
                new_state = ((nx, ny), cleaned)
                heapq.heappush(pq, (
                    g + 1 + heuristic(new_state),
                    g + 1,
                    new_state,
                    path + [("move", (nx, ny))]
                ))

    return None, float("inf")
