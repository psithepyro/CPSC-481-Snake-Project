REQUIRED INSTALLS:
pygame - #pip install pygame
matplotlib - #python -m pip install -U matplotlib
psutil - #pip install psutil
#
#
#
#
The project is split up into 4 main files:
snake_game.py, snake_search.py, plot_eval.py, and main.py 

snake_game.py contains the game logic for the snake game. It uses pygame and random to create the game elements such as the snake, food, and score. It also handles adds the logic for the snake to move and the game to end.

snake_search.py contains the assortment of search algorithms for the snake game. It uses A*, IDDFS, BFS, and UCS as search algorithms to evaluate their performance in the game. It also contains the evaluation parameters each algorithm at the end of the game.

plot_eval.py contains the code to plot the evaluation parameters for each algorithm. It uses matplotlib along with numpy to  help create the graphs to visualize the results.

The main.py file is the entry point of the project and it calls the functions from the other files
from here you are able to run the project by running the main.py file.
You are also able to adjust the number of simulations in the main.py file if needed.

