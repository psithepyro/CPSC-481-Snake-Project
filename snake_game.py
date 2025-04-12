import pygame
import random
from collections import deque, defaultdict




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
YELLOW = (255, 255, 0)

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

    def draw(self, screen, path=None):
        # Draw the game background
        screen.fill(BLACK)
        # Draw the border
        pygame.draw.rect(screen, BLUE, (MARGIN, MARGIN, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 2)

        # Draw the snake's search path in yellow
        if path:
            for step in path:
                pygame.draw.rect(screen, YELLOW, (step[0] * GRID_SIZE + MARGIN, step[1] * GRID_SIZE + MARGIN, GRID_SIZE, GRID_SIZE))

        # Draw the snake
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE + MARGIN, segment[1] * GRID_SIZE + MARGIN, GRID_SIZE, GRID_SIZE))
        
        
        # Draw the food
        pygame.draw.rect(screen, RED, (self.food[0] * GRID_SIZE + MARGIN, self.food[1] * GRID_SIZE + MARGIN, GRID_SIZE, GRID_SIZE))

        # Render score, length, and timer
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Calculate elapsed time in seconds
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, WHITE)
        algorithm_text = self.font.render(f"Algorithm: {self.current_algorithm}", True, WHITE)

        # Draw the text for score and timer on the screen
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 25))
        screen.blit(algorithm_text, (250, 20))
        # Update the display
        pygame.display.flip()

