import pygame
import random
from collections import deque
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
BLUE = (0, 0, 255)  # Border color

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
        self.font = pygame.font.SysFont(None, 24)  # Font for rendering text
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

        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 25))

        # Update the display
        pygame.display.flip()


def bfs(game):
    start = game.snake[0]
    target = game.food
    # Initialize the queue with the start position and an empty path
    queue = deque([(start, [])])
    visited = set()

    while queue:
        # Pop the first element from the queue
        (x, y), path = queue.popleft()
        # If the current position is the target, return the path
        if (x, y) == target:
            return path
        # If the current position has been visited, skip it
        if (x, y) in visited:
            continue
        # Mark the current position as visited
        visited.add((x, y))

        # Add the adjacent positions to the queue
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            nx, ny = x + dx, y + dy
            # If the adjacent position is valid and not in the snake body, add it to the queue
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in game.snake:
                queue.append(((nx, ny), path + [(dx, dy)]))
    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = SnakeGame()

    while not game.game_over:
        path = bfs(game)  # Use BFS to find the path
        if path:
            game.direction = path[0]  # Move in the first direction of the path

        game.move()
        game.draw(screen)
        clock.tick(50)  # Control game speed

    print(f"Game Over! Score: {game.score}")
    print(f"Time: {(pygame.time.get_ticks() - game.start_time) // 1000}s")
    pygame.quit()

if __name__ == "__main__":
    main()