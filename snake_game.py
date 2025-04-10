import pygame
import random
import os
import psutil #pip install psutil; if psutil not installed run this command in the terminal
import heapq
from collections import deque, defaultdict
import time
import matplotlib.pyplot as plt #python -m pip install -U matplotlib; if matplotlib not installed run this command in the terminal
import numpy as np


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
    def __init__(self, alg):
        # Initialize the game components
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.SysFont(None, 24)
        self.start_time = pygame.time.get_ticks()  # Store the start time
        self.current_algorithm = alg

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
        
        algorithm_text = self.font.render(f"Algorithm: {self.current_algorithm}", True, WHITE)

        # Draw the text for score and text on the screen
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 25))
        screen.blit(algorithm_text, (250, 20))
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
        # Initializes a double ended queue with the start position and an empty path
        open_list = [(0, start, [])]  # Priority queue: (f_score, position, path)
        visited = set()
        max_nodes = 0
        while open_list:
            # Update the maximum number of nodes expanded
            max_nodes = max(max_nodes, len(open_list))
            # Pop the node with the lowest f_score
            f,(x, y), path = heapq.heappop(open_list)
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
                    # Total cost 
                    totalnode_Cost = node_cost
                    heapq.heappush(open_list, (totalnode_Cost, (nx, ny), new_path))

        return None, max_nodes 

    def iter_deepening(game):
        start = game.snake[0]
        target = game.food
        max_depth = GRID_WIDTH * GRID_HEIGHT
        max_nodes_overall = 0
        
        # Iteratively increase the depth limit
        for depth_limit in range(1, max_depth + 1):
            visited = set()
            stack = deque([(start, [], 0)]) # Stack for IDS: (position, path, depth)
            max_nodes = 0
            
            while stack:
                max_nodes = max(max_nodes, len(stack))
                (x, y), path, depth = stack.pop()
                
                # If the current position is the food then return the path 
                # Along with the maximum number of nodes expanded 
                if (x, y) == target:
                    return path, max(max_nodes, max_nodes_overall)
                
                # Will skip if depth limit reached 
                if depth >= depth_limit:
                    continue

                # If the current position has been visited, skip it
                visited.add((x, y))
                
                # Add the adjacent positions to the stack
                for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                    nx, ny = x + dx, y + dy
                    # If the adjacent position have not been visited and not in the snake body, add it to the stack
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake and (nx, ny) not in visited:
                        stack.append(((nx, ny), path + [(dx, dy)], depth + 1))
            
            max_nodes_overall = max(max_nodes_overall, max_nodes)
            
            # If solution is not found in this iteration it will increase the depth limit by 1 
        return None, max_nodes_overall
    

def plot_results(results):
    algorithms = list(results.keys())
    # Prepare data for plotting
    metrics = {
        'Score': [np.mean(results[alg]["scores"]) for alg in algorithms],
        'Time': [np.mean(results[alg]["times"]) for alg in algorithms],
        'Max Nodes': [np.mean(results[alg]["max_nodes"]) for alg in algorithms],
        'Memory (MB)': [np.mean(results[alg]["mem_usage"]) for alg in algorithms]
    }
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Algorithm Performance Comparison', fontsize=16)
    
    # Plot each metric
    for i, (metric_name, values) in enumerate(metrics.items()):
        ax = axes[i//2, i%2]
        bars = ax.bar(algorithms, values, color=plt.cm.Paired(np.arange(len(algorithms))))
        ax.set_title(metric_name)
        ax.set_ylabel(metric_name)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        # Rotate algorithm names if they're long
        plt.sca(ax)
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison.png')  # Save to file
    plt.show()

def main(algorithms, num_simulations=1):
    # Initialize Pygame to run simulations 
    pygame.init()  
    # Using a dictionary to store the results of the simulations for each algorithm 
    results = defaultdict(lambda: {"scores": [], "times": [], "max_nodes": [], "mem_usage": []})
    # Initialize the Pygame clock and screen to visualize the game and its tick rate
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    total_trials = 1

    # Run the simulations using the specified search algorithms
    for alg in algorithms:
        # Run the simulation num_simulations times
        for i in range(num_simulations):
            # Initialize the game and start the timer
            game = SnakeGame(alg.__name__.upper())
            start_time = time.time()
            max_nodes = 0
            peak_mem = 0
            # Initialize the memory usage
            time.sleep(0.1)  # Allow time for the process to start
            process = psutil.Process(os.getpid())
            init_mem = process.memory_info().rss / (1024 * 1024)  # Memory usage calculated in MB

            # Initialize the search algorithm 
            while not game.game_over:
                # Keep track of the memory usage before alg execution
                current_mem = process.memory_info().rss / (1024 * 1024)
                peak_mem = max(peak_mem, current_mem)  # Calculate peak memory usage

                # Track the maximum number of nodes expanded in the search
                path, current_max_nodes = alg(game)

                # Check if the algorithm is taking too long (timeout after 60 seconds)
                elapsed_time = time.time() - start_time
                if elapsed_time > 60:
                    print(f"{alg.__name__} snake trial {i+1}: Timeout after 60 seconds.")
                    print("-" * 60)
                    game.game_over = True
                    break

                # Update the maximum number of nodes expanded
                max_nodes = max(max_nodes, current_max_nodes)

                # If a path is found, move the snake in the specified direction
                if path:
                    game.direction = path[0]

                # Move the snake and update the game state
                game.move()
                clock.tick(200)
                game.draw(screen)

            # Store the score and time taken for the current trial
            end_time = time.time()
            final_mem = process.memory_info().rss / (1024 * 1024)
            if total_trials == 1:
                mem_used = peak_mem - init_mem - 0.55  # Memory used during the simulation
            else:
                mem_used = peak_mem - init_mem  # Memory used during the simulation
            total_trials += 1

            # If the simulation timed out, record a score of 0 and skip further calculations
            if elapsed_time > 60:
                results[alg.__name__]["scores"].append(game.score)
                results[alg.__name__]["times"].append(60)
                results[alg.__name__]["max_nodes"].append(max_nodes)
                results[alg.__name__]["mem_usage"].append(mem_used)

                print(f"{alg.__name__} snake trial {i+1}: Score = {game.score}, Time = {60.00:.2f}s, Max Nodes = {max_nodes}, Memory Used = {mem_used:.2f}MB")
                print("-" * 100)
                continue

            results[alg.__name__]["scores"].append(game.score)
            results[alg.__name__]["times"].append(end_time - start_time)
            results[alg.__name__]["max_nodes"].append(max_nodes)
            results[alg.__name__]["mem_usage"].append(mem_used)

            # Print the score and time for the current trial
            print(f"{alg.__name__} snake trial {i+1}: Score = {game.score}, Time = {end_time - start_time:.2f}s, Max Nodes = {max_nodes}, Memory Used = {mem_used:.2f}MB")
            print("-" * 100)

    print("\n \t\t\t---Simulation Results---")
    print(f"{'Algorithm':<18}{'Avg Score':<14}{'Avg Time':<12}{'Avg Max Nodes':<15}{'Avg Memory Use (MB)':<12}")
    print("-" * 100)

    # Print the average score and time for each algorithm
    for alg, data in results.items():
        avg_score = sum(data["scores"]) / num_simulations
        avg_time = sum(data["times"]) / num_simulations
        avg_max_nodes = sum(data["max_nodes"]) / num_simulations
        avg_mem = sum(data["mem_usage"]) / num_simulations

        print(f"{alg:<18} {avg_score:<14.2f} {avg_time:<12.2f} {avg_max_nodes:<12.2f} {avg_mem:<15.2f}")
        print("-" * 80)

    return results

if __name__ == "__main__":
    results = main([Snake_Search.bfs, Snake_Search.a_star, Snake_Search.ucs, Snake_Search.iter_deepening], num_simulations=200)
    plot_results(results)
