import pygame
import random
import sys
import heapq
from collections import deque, defaultdict
import time


# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
MARGIN = 50 
GRID_WIDTH = (WIDTH - MARGIN) // GRID_SIZE
GRID_HEIGHT = (HEIGHT - MARGIN) // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        # Initialize the game components
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.SysFont(None, 24)
        self.start_time = pygame.time.get_ticks()  # Store the start time

    def generate_food(self):
        # Generate a new food at a random position
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def move(self):
        #Initialize the new head of the snake
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        # Check if the snake eats the food
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.food = self.generate_food()
            self.score += 1
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        # Check if the snake collides with the wall or itself
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake[1:]):
            self.game_over = True

    def draw(self, screen):
        # Draw the game background
        screen.fill(BLACK)
        # Draw the border
        pygame.draw.rect(screen, BLUE, (MARGIN, MARGIN, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 2)

        # Draw the snake and food
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE + MARGIN, segment[1] * GRID_SIZE + MARGIN, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (self.food[0] * GRID_SIZE + MARGIN, self.food[1] * GRID_SIZE + MARGIN, GRID_SIZE, GRID_SIZE))
        
        # Render score, length, and timer
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        # Calculate elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000 
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, WHITE)

        # Draw the text for score and text on the screen
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 25))
        
        # Update the display
        pygame.display.flip()

class Snake_Search:
    
    def heuristic(a, b): 
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def bfs(game):
        start = game.snake[0]
        target = game.food
        # Initializes a double ended queue with the start position and an empty path
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
                return path, max_nodes
            # If the current position has been visited, skip it
            if (x, y) in visited:
                continue
            # Mark the current position as visited
            visited.add((x, y))

            # Add the adjacent positions to the double ended queue
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                # Calculate the next position
                nx, ny = x + dx, y + dy
                # If the adjacent position is valid and not in the snake body, add it to the queue
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake:
                    queue.append(((nx, ny), path + [(dx, dy)]))
        return None, max_nodes
    
    def dfs(game):
        start = game.snake[0]
        target = game.food
        stack = [(start, [])]
        visited = set()
        max_nodes = 0

        while stack:
            max_nodes = max(max_nodes, len(stack))
            (x, y), path = stack.pop()
            if (x, y) == target:
                return path, max_nodes
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                # Avoid walls and body
                if (0 <= nx < GRID_WIDTH and 
                    0 <= ny < GRID_HEIGHT and 
                    (nx, ny) not in game.snake):
                    stack.append(((nx, ny), path + [(dx, dy)]))
        return None, max_nodes
    
    def a_star(game):
        start = game.snake[0]
        target = game.food
        open_list = [(0, start, [])]  # Priority queue: (f_score, position, path)
        visited = set()
        max_nodes = 0

        while open_list:
            # Update the maximum number of nodes expanded
            max_nodes = max(max_nodes, len(open_list))
            # Pop the node with the lowest f_score
            f, (x, y), path = heapq.heappop(open_list)
            # If the current position is the target, return the path and max_nodes
            if (x, y) == target:
                return path, max_nodes
            # If the current position has been visited, skip it
            if (x, y) in visited:
                continue
            # Mark the current position as visited
            visited.add((x, y))

            # Add the adjacent positions to the priority queue
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake and (nx, ny) not in visited:
                    new_path = path + [(dx, dy)]
                    # Cost to reach this node
                    node_cost = len(new_path)  
                    # Heuristic cost to the target
                    heur = Snake_Search.heuristic((nx, ny), target) 
                    # Total cost 
                    totalnode_Cost = node_cost + heur  # Total cost
                    heapq.heappush(open_list, (totalnode_Cost, (nx, ny), new_path))

        return None, max_nodes
    
    def ucs(game):
        start = game.snake[0]
        target = game.food
        open_list = [(0, start, [])] #
        visited = set()
        max_nodes = 0

        while open_list:
            # Track priority queue size
            max_nodes = max(max_nodes, len(open_list))  
            cost, (x, y), path = heapq.heappop(open_list)
            if (x, y) == target:
                return path, max_nodes
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake:
                    new_path = path + [(dx, dy)]
                    new_cost = cost + 1
                    heapq.heappush(open_list, (new_cost, (nx, ny), new_path))
        return None, max_nodes
    


def main(algorithms, num_simulations=5):
    # Initialize Pygame to run simulations 
    pygame.init()  
    # Store the results of the simulations for each algorithm
    results = defaultdict(lambda: {"scores": [], "times": [], "max_nodes": []})
    # Initialize the Pygame clock and screen to visualize the game and its tick rate
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #Run the simulations using the specified search algorithms
    for alg in algorithms:
        # Run the simulation num_simulations times
        for i in range(num_simulations):
            # Initialize the game and start the timer
            game = SnakeGame()
            start_time = time.time()
            max_nodes = 0

            #Initialize the search algorithm 
            while not game.game_over:
                #track the maximum number of nodes expanded in the search
                if alg.__name__ == "bfs":
                    path, current_max_nodes = alg(game)
                elif alg.__name__ == "dfs":
                    path, current_max_nodes = alg(game)
                elif alg.__name__ == "a_star":
                    path, current_max_nodes = alg(game)
                elif alg.__name__ == "ucs":
                    path, current_max_nodes = alg(game)

                # Update the maximum number of nodes expanded
                max_nodes = max(max_nodes, current_max_nodes)

                # If a path is found, move the snake in the specified direction
                if path:
                    game.direction = path[0] # Exit the loop if no path is found

                # Move the snake and update the game state
                game.move()
                clock.tick(200)
                game.draw(screen)

            # Store the score and time taken for the current trial
            end_time = time.time()
            results[alg.__name__]["scores"].append(game.score)
            results[alg.__name__]["times"].append(end_time - start_time)
            results[alg.__name__]["max_nodes"].append(max_nodes)

            # Print the score and time for the current trial
            print(f"{alg.__name__} snake trial {i+1}: Score = {game.score}, Time = {end_time - start_time:.2f}s, Max Nodes = {max_nodes}")
            print("-" * 70)

    print("\n \t\t---Simulation Results---")
    print(f"{'Algorithm':<18}{'Avg Score':<14}{'Avg Time':<12} {'Avg Max Nodes':<12}")
    print("-" * 60)

    # Print the average score and time for each algorithm
    for alg, data in results.items():
        avg_score = sum(data["scores"]) / num_simulations
        avg_time = sum(data["times"]) / num_simulations
        avg_max_nodes = sum(data["max_nodes"]) / num_simulations
        print(f"{alg:<18} {avg_score:<14.2f} {avg_time:<12.2f} {avg_max_nodes:<12.2f}")
        print("-" * 60)

if __name__ == "__main__":
    main([Snake_Search.bfs,Snake_Search.a_star, Snake_Search.ucs], num_simulations=10)