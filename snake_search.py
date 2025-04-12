import heapq
from collections import deque
from snake_game import UP, DOWN, LEFT, RIGHT, GRID_WIDTH, GRID_HEIGHT

class Snake_AI:
    
    def heuristic(a, b):
        # Manhattan distance (simpler and faster)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def bfs(game):
        start = game.snake[0]
        target = game.food
        # Initializes a double-ended queue with the start position and an empty path (FIFO)
        queue = deque([(start, [])])
        visited = set()
        max_nodes = 0

        while queue:
            # Update the maximum number of nodes expanded
            max_nodes = max(max_nodes, len(queue))
            # Pop the first element from the queue
            (x, y), path = queue.popleft()
            # If the current position is the target, return the path
            if (x, y) == target:
                return [start] + path, max_nodes
            # If the current position has been visited, skip it
            if (x, y) in visited:
                continue
            # Mark the current position as visited
            visited.add((x, y))

            # Add the adjacent positions to the double-ended queue
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                # Calculate the next position
                nx, ny = x + dx, y + dy
                # If the adjacent position is valid and not in the snake body, add it to the queue
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return None, max_nodes

    def a_star(game):
        start = game.snake[0]
        target = game.food
        open_list = [(0, start)]  # Priority queue: (f_score, position) 
        g_score = {start: 0}  # Cost to reach each node
        came_from = {}  # To reconstruct the path
        visited = set()
        max_nodes = 0

        while open_list:
            # Update the maximum number of nodes expanded
            max_nodes = max(max_nodes, len(open_list))
            # Pop the node with the lowest f_score
            f_score, current = heapq.heappop(open_list)
            # If the current position is the target, reconstruct the path
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return [start] + path, max_nodes
            # If the current position has been visited, skip it
            if current in visited:
                continue
            # Mark the current position as visited
            visited.add(current)

            # Add the adjacent positions to the priority queue
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                # Calculate the next position
                neighbor = (current[0] + dx, current[1] + dy)
                # If the adjacent position is valid and not in the snake body, add it to the queu
                if 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT and neighbor not in game.snake:
                    tentative_g_score = g_score[current] + 1  # Cost to reach this neighbor

                    # If this path is better, update the g_score and push to the queue
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + Snake_AI.heuristic(neighbor, target)
                        heapq.heappush(open_list, (f_score, neighbor))
                        came_from[neighbor] = current

        return None, max_nodes
    
    def ucs(game):
        start = game.snake[0]
        target = game.food
        # Initializes a priority queue with the start position and an empty path
        open_list = [(0, start, [])]  # Priority queue: (cost, position, path)
        visited = set()
        max_nodes = 0

        while open_list:
            # Update the maximum number of nodes expanded
            max_nodes = max(max_nodes, len(open_list))
            # Pop the node with the lowest cost
            cost, (x, y), path = heapq.heappop(open_list)
            # If the current position is the target, return the path
            if (x, y) == target:
                return [start] + path, max_nodes
            # If the current position has been visited, skip it
            if (x, y) in visited:
                continue
            # Mark the current position as visited
            visited.add((x, y))

            # Add the adjacent positions to the priority queue
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake and (nx, ny) not in visited:
                    new_path = path + [(nx, ny)]
                    heapq.heappush(open_list, (cost + 1, (nx, ny), new_path))
        return None, max_nodes

    def iter_deepening(game):
        start = game.snake[0]
        target = game.food
        max_depth = GRID_WIDTH * GRID_HEIGHT
        max_nodes_overall = 0

        # Iteratively increase the depth limit
        for depth_limit in range(1, max_depth + 1):
            visited = set()
            stack = deque([(start, [], 0)])  # Stack for IDS: (position, path, depth)
            max_nodes = 0

            while stack:
                max_nodes = max(max_nodes, len(stack))
                (x, y), path, depth = stack.pop()

                # If the current position is the target, return the path
                if (x, y) == target:
                    return [start] + path, max(max_nodes, max_nodes_overall)

                # Skip if depth limit is reached
                if depth >= depth_limit:
                    continue

                # Mark the current position as visited
                visited.add((x, y))

                # Add the adjacent positions to the stack
                for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                    nx, ny = x + dx, y + dy
                    # Only add valid positions that are not visited and not part of the snake's body
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake and (nx, ny) not in visited:
                        stack.append(((nx, ny), path + [(nx, ny)], depth + 1))

            max_nodes_overall = max(max_nodes_overall, max_nodes)

        # If no solution is found, return None
        return None, max_nodes_overall