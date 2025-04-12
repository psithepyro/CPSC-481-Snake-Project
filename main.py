import pygame
import os
import psutil #pip install psutil; if psutil not installed run this command in the terminal
from collections import defaultdict
import snake_search # Import the search algorithms from snake_search.py
import snake_game # Import the SnakeGame class from snake_game.py
import plot_eval # Import the plot_results function from plot_eval.py
from snake_game import UP, DOWN, LEFT, RIGHT, GRID_WIDTH, GRID_HEIGHT, WIDTH, HEIGHT
import time


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
            game = snake_game.SnakeGame(alg.__name__.upper())
            start_time = time.time()
            max_nodes = 0
            peak_mem = 0
            # Initialize the memory usage
            time.sleep(0.1)  # Allow time for the process to start
            process = psutil.Process(os.getpid())
            init_mem = process.memory_info().rss / (1024 * 1024)  # Memory usage calculated in MB

            # Initialize the search algorithm 
            while not game.game_over:
                # Check if 3 seconds have passed without scoring 10 points
                elapsed_time = time.time() - start_time
                if elapsed_time > 3 and game.score <= 10:
                    print(f"{alg.__name__} snake trial {i+1}: Restarting simulation due to timeout.")
                    print("-" * 75)
                    game = snake_game.SnakeGame(alg.__name__.upper())
                    start_time = time.time()
                    max_nodes = 0
                    peak_mem = 0
                    # Initialize the memory usage
                    time.sleep(0.1)  # Allow time for the process to start
                    process = psutil.Process(os.getpid())
                    init_mem = process.memory_info().rss / (1024 * 1024)  

                # Keep track of the memory usage before alg execution
                current_mem = process.memory_info().rss / (1024 * 1024)
                peak_mem = max(peak_mem, current_mem)  # Calculate peak memory usage

                # Track the maximum number of nodes expanded in the search
                path, current_max_nodes = alg(game)

                # Update the maximum number of nodes expanded
                max_nodes = max(max_nodes, current_max_nodes)

                # If a path is found, move the snake in the specified direction
                if path:
                    game.direction = (path[1][0] - path[0][0], path[1][1] - path[0][1])  # Calculate direction from the path
                else:
                    # Fallback to a safe move
                    head = game.snake[0]
                    for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                        nx, ny = head[0] + dx, head[1] + dy
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake:
                            game.direction = (dx, dy)
                            break

                # Move the snake and update the game state
                game.move()
                clock.tick(200)
                game.draw(screen, path)  # Pass the path to the draw method

            # If the game was restarted, skip storing results
            if elapsed_time > 3 and game.score <= 10:
                continue

            # Store the score and time taken for the current trial
            end_time = time.time()
            final_mem = process.memory_info().rss / (1024 * 1024)
            if total_trials == 1:
                mem_used = peak_mem - init_mem - 0.5  # Memory used during the simulation
            else:
                mem_used = peak_mem - init_mem  # Memory used during the simulation
            total_trials += 1

            results[alg.__name__]["scores"].append(game.score)
            results[alg.__name__]["times"].append(end_time - start_time)
            results[alg.__name__]["max_nodes"].append(max_nodes)
            if mem_used <= 0:
                mem_used = 0.01  # Avoid zero memory usage

            # Print the score and time for the current trial
            results[alg.__name__]["mem_usage"].append(mem_used)
            print(f"{alg.__name__} snake trial {i+1}: Score = {game.score}, Time = {end_time - start_time:.2f}s, Max Nodes = {max_nodes}, Memory Used = {mem_used:.2f}MB")
            print("-" * 100)

            
    print("\n \t\t\t---Simulation Results---")
    print(f"{'Algorithm':<18}{'Avg Score':<15}{'Avg Time':<13}{'Avg Max Nodes':<17}{'Avg Memory Use (MB)':<14}")
    print("-" * 100)

    # Print the average score and time for each algorithm
    for alg, data in results.items():
        avg_score = sum(data["scores"]) / num_simulations
        avg_time = sum(data["times"]) / num_simulations
        avg_max_nodes = sum(data["max_nodes"]) / num_simulations
        avg_mem = sum(data["mem_usage"]) / num_simulations

        print(f"{alg:<18} {avg_score:<15.2f} {avg_time:<13.2f} {avg_max_nodes:<17.2f} {avg_mem:<14.2f}")
        print("-" * 80)

    return results

if __name__ == "__main__":
    results = main([snake_search.Snake_AI.bfs, snake_search.Snake_AI.a_star, snake_search.Snake_AI.ucs,snake_search.Snake_AI.iter_deepening], num_simulations=2)
    plot_eval.plot_results(results)