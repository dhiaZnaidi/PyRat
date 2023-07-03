# Introduction 

The PyRat software can be installed on Linux, MacOS and Windows. Based on your choice (which should be Linux 😉 ), follow the instructions in the corresponding section below.

# Dependencies : 
In order for the code to work, you need to install these modules : 

`!pip install ipynb-py-convert pygame gdown heapq`

# Launching the game : 

To start the game, you have certain options : 

```
options:
  -h, --help            show this help message and exit

  --rat rat_file        Program to control the rat (local file or Google Colab shared link)

  --python python_file  Program to control the python (local file or Google Colab shared link)
  -x x, --width x       Width of the maze
  -y y, --height y      Height of the maze
  -d d, --density d     Targetted density of walls
  -p p, --pieces p      Number of pieces of cheese
  --nonsymmetric        Do not enforce symmetry of the maze
  -md md, --mud_density md
                        Mud density
  -mr mr, --mud_range mr
                        Mud range (mud is between 2 and mr)
  --nonconnected        Does not enforce connectivity of the maze
  --preparation_time pt
                        Preparation time in milliseconds
  --turn_time tt        Turn time in milliseconds
  --window_width ww     Window width (in pixels)
  --auto_exit           Automatically exit when game is finished (useful for scripts)
  --desactivate_animations
                        Desactivate animations (for slower systems)
  --synchronous         Wait for players
  -mt mt, --max_turns mt
                        Max number of turns
  --nodrawing           Desactivate drawing
  --save_images         Draw in images instead of in window
  --tests tests         Number of tests (for statistics)
  --maze_file maze_file
                        Specific maze file to load
  --fullscreen          Start game in fullscreen (you can press the "f" key instead)
  --debug debug_level   Debug level
  --start_random        Players start at random location in the maze
  --save                Save game to file (for ML-based solutions)
  --save_match          Save game to directory (for replaying later)
  --load_match match_dir
                        Directory containing the match to load
  --random_seed random_seed
                        random seed to use in order to generate a specific maze
  --random_cheese       Force cheese location to be random (even if used in combination with --random_seed)
  --postprocessing      Perform postprocessing (useful for tournaments)
  --import_keras        Import keras when loading pyrat to avoid multiple
                        loads
```

You can check them by running :

`python pyrat.py -h`

You can choose to run a single player mode or two players mode by specifying the python file and the rat file.

To run the 2 players mode you can execute the following code : 

`python .\pyrat.py --rat '.\IA Pyrat\IA avec centre.ipynb' --python '.\IA Pyrat\IA sans Centre.ipynb' -x 31 -y 29 -p 41 -d 0.4 -md 0.1`

# After the game : 

Once the game is finished, a string of characters appears in the terminal, summarizing the game:

It contains a certain amount of information for each player, among which :
```
miss_xxx: The number of movements missed due to a too long calculation or moving toward a wall;
moves_xxx: The number of moves performed (and not missed);
prep_time_xxx: The time effectively taken by function preprocessing before completing;
score_xxx: The number of pieces of cheese collected;
stucks_xxx: The number of additional movements caused by mud;
turn_time_xxx: The time effectively taken by function turn before returning a move;
win_xxx: 1 if the game is won, 0 if lost, 0.5 if tied.
```
To obtain average statistics on several games (which is interesting, especially if they contain some random factor), use the `--tests parameter`. The PyRat output will indicate the average obtained for each of the criteria mentioned above.

You should use it in combination with `--nodrawing --synchronous` for faster computations.