# %%
"""
<h1><b><center>How to use this file with PyRat?</center></b></h1>
"""

# %%
"""
Google Colab provides an efficient environment for writing codes collaboratively with your group. For us, teachers, it allows to come and see your advancement from time to time, and help you solve some bugs if needed.

The PyRat software is a complex environment that takes as an input an AI file (as this file). It requires some resources as well as a few Python libraries, so we have installed it on a virtual machine for you.

PyRat is a local program, and Google Colab is a distant tool. Therefore, we need to indicate the PyRat software where to get your code! In order to submit your program to PyRat, you should follow the following steps:

1.   In this notebook, click on *Share* (top right corner of the navigator). Then, change sharing method to *Anyone with the link*, and copy the sharing link;
2.   On the machine where the PyRat software is installed, start a terminal and navigate to your PyRat directory;
3.   Run the command `python ./pyrat.py --rat "<link>" <options>`, where `<link>` is the share link copied in step 1. (put it between quotes), and `<options>` are other PyRat options you may need.
"""

# %%
"""
<h1><b><center>Pre-defined constants</center></b></h1>
"""

# %%
"""
A PyRat program should -- at each turn -- decide in which direction to move. This is done in the `turn` function later in this document, which should return one of the following constants:
"""

# %%
"""
# **The number of our group: Groupe N2 Equipe 10**
# **The name of our AI: Gammoudi**
# **The name of our team: Chekmate**
# **The names of its members: Znaidi Dhia/ Ben Ismail Rayen/ Gelfert Thomas**

"""

# %%
import heapq

# %%
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

# %%
pieces=[]
moves=[]
eaten_pieces=[]
moving=False
meta_graph = {}
best_paths = {}
testing={}
path_to_new_target=[]
is_following_me=0
is_matched=0
consider_as_eaten=[]
tempted=tuple()

# %%
"""
<h1><b><center>Your coding area</center></b></h1>
"""

# %%
"""
Please put your functions, imports, constants, etc. between this text and the PyRat functions below. You can add as many code cells as you want, we just ask that you keep things organized (one function per cell, commented, etc.), so that it is easier for the teachers to help you debug your code!
"""

# %%
def move_from_locations_step (source_location, target_location) : 
    difference = (target_location[0] - source_location[0], target_location[1] - source_location[1])
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else :
        raise Exception("Impossible move")

# %%

def create_structure():
    return []
    #Create a minheap

def empty(structure):
    return structure == []

def add_or_replace (structure, element) :
    heapq.heappush(structure, element) #element = (key(vertex), value(distance from initial vertex))
    # Add an element to the minheap

def remove (structure) :
    #Before executing the function, we check wether our structure is an empty list or not
    assert structure != [] 
    return heapq.heappop(structure)
    # remove an element from the minheap

# %%
def Dijkstra (graph,start_vertex) :

    # Initialize structure with initial vertex, at distance 0, with no predecessor
    queuing_structure = create_structure()
    add_or_replace(queuing_structure, (0, start_vertex, None))

    # Initialize routing (main difference with course is we also store the length of paths stored with explored vertices)
    explored_vertices = {}
    routing_table = {}

    # Loop until all vertices have been explored
    while len(queuing_structure) > 0 :

        # Pop next vetex to visit
        (distance_to_current_vertex, current_vertex, parent) = remove(queuing_structure)
        if current_vertex not in explored_vertices :

            # Store route to it
            explored_vertices[current_vertex] = distance_to_current_vertex
            routing_table[current_vertex] = parent

            # Add its its neighbors to the structure for later consideration
            for neighbor in graph[current_vertex] :
                if neighbor not in explored_vertices : 
                    distance_to_neighbor = distance_to_current_vertex + graph[current_vertex][neighbor]
                    add_or_replace(queuing_structure, (distance_to_neighbor, neighbor, current_vertex))
    
    # Return shortest paths and routing table
    return explored_vertices, routing_table

# %%
def find_route (routing_table, source_location, target_location) :

    # Return a sequence of locations from source to target using provided routing table
    route = [target_location]
    while route[0] != source_location :
        route.insert(0, routing_table[route[0]])
    return route

# %%
def order_by_nearest(dictionary):
    reverse={j:i for i,j in dictionary.items()}
    a=list(dictionary.values())
    a.sort()
    return {reverse[i]:i for i in a}

# %%
def build_meta_graph (mazeMap, pieces_of_cheese):
    
    all_locations = pieces_of_cheese
    metaGraph = {}
    bestPaths  = {}

    i = len(all_locations)-1
    while i >= 0:
        
        explored_vertices,routing_table = Dijkstra(mazeMap,all_locations[i])

        j = 0
        while j < i:

            if all_locations[i] not in bestPaths :
                bestPaths[all_locations[i]] = {}
                metaGraph[all_locations[i]] = {}
                
            if all_locations[j] not in bestPaths :
                bestPaths[all_locations[j]] = {}
                metaGraph[all_locations[j]] = {}

            if not metaGraph[all_locations[j]].get(all_locations[i], False):
                path = find_route(routing_table, all_locations[i], all_locations[j])
                distance = explored_vertices[all_locations[j]]

                metaGraph[all_locations[i]][all_locations[j]] = distance
                bestPaths[all_locations[i]][all_locations[j]] = path

                metaGraph[all_locations[j]][all_locations[i]] = distance
                bestPaths[all_locations[j]][all_locations[i]] = path[::-1]

            j += 1
        
        i -= 1
    metaGraph={i:order_by_nearest(metaGraph[i]) for i in metaGraph.keys()}    
    return metaGraph, bestPaths

# %%
def updatepieces (metaGraph,location):
    test=False
    if location in metaGraph :
        eaten_pieces.append(location)
        test=True
    return eaten_pieces,test

# %%
def find_closest_piece_of_cheese(graph,current_position,remaining):
    distances,routing_table=Dijkstra(graph,current_position)
    weight={i:distances[i] for i in remaining}
    order=order_by_nearest(weight)
    closest_piece_of_cheese=list(order.keys())[0]
    chemin=find_route(routing_table,current_position,closest_piece_of_cheese)
    return closest_piece_of_cheese,chemin

# %%
def move_from_locations(locations):
    if len(locations)<2:
        pass
    else:
        move_to_apply=move_from_locations_step(locations[0],locations[1])
        locations.pop(0)
        return move_to_apply

# %%
"""
<h1><b><center>PyRat functions</center></b></h1>
"""

# %%
"""
The `preprocessing` function is called at the very start of a game. It is attributed a longer time compared to `turn`, which allows you to perform intensive computations. If you store the results of these computations into **global** variables, you will be able to reuse them in the `turn` function.

*Input:*
*   `maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][(0, 1)]`.
*   `maze_width` -- **int** -- The width of the maze, in number of cells.
*   `maze_height` -- **int** -- The height of the maze, in number of cells.
*   `player_location` -- **pair(int, int)** -- The initial location of your character in the maze.
*   `opponent_location` -- **pair(int,int)** -- The initial location of your opponent's character in the maze.
*   `pieces_of_cheese` -- **list(pair(int, int))** -- The initial location of all pieces of cheese in the maze.
*   `time_allowed` -- **float** -- The time you can take for preprocessing before the game starts checking for moves.

*Output:*
*   This function does not output anything.
"""

# %%
def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global meta_graph, best_paths,pieces
    pieces=pieces_of_cheese[:]
    meta_graph,best_paths=build_meta_graph (maze_map, pieces_of_cheese)
    
    

# %%
"""
The `turn` function is called each time the game is waiting
for the player to make a decision (*i.e.*, to return a move among those defined above).

*Input:*
*   `maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze. It is the same as in the `preprocessing` function, just given here again for convenience.
*   `maze_width` -- **int** -- The width of the maze, in number of cells.
*   `maze_height` -- **int** -- The height of the maze, in number of cells.
*   `player_location` -- **pair(int, int)** -- The current location of your character in the maze.
*   `opponent_location` -- **pair(int,int)** -- The current location of your opponent's character in the maze.
*   `player_score` -- **float** -- Your current score.
*   `opponent_score` -- **float** -- The opponent's current score.
*   `pieces_of_cheese` -- **list(pair(int, int))** -- The location of remaining pieces of cheese in the maze.
*   `time_allowed` -- **float** -- The time you can take to return a move to apply before another time starts automatically.

*Output:*
*   A chosen move among `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT` or `MOVE_RIGHT`.
"""

# %%

def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global meta_graph,eaten_pieces,testing,path_to_new_target,pieces,is_following_me
    global moving
    global tempted,is_matched
    # Si l'ennemi mange une pièce de fromage et que je n'y suis pas, on la compte
    eaten_pieces,test = updatepieces (meta_graph,opponent_location)

    # Si une pièce de fromage a été mangée, on la compte
    eaten_pieces,_ = updatepieces (meta_graph,player_location)
    listcheese=list(set(pieces)-set(eaten_pieces))

    if moving: 
        if (not path_to_new_target) or (test and testing[-1]==eaten_pieces[-1]) or (is_following_me==3) :
                is_following_me=0
                moving = False
    if not moving:
        if is_matched==3 and opponent_score>player_score:
            is_matched=0
            listcheese.remove(tempted)
            new_target,path_to_new_target=find_closest_piece_of_cheese(maze_map,player_location,listcheese)
            moving=True
            testing=path_to_new_target
            path_to_new_target.pop(0)
        else:
            new_target,path_to_new_target=find_closest_piece_of_cheese(maze_map,player_location,listcheese)
            tempted=new_target
            testing=path_to_new_target
            path_to_new_target.pop(0)
            moving = True
            if len(path_to_new_target)>=3:
                if opponent_location in [path_to_new_target[1],path_to_new_target[2]]:
                    is_following_me+=1
            else:
                is_following_me=3
            if opponent_location==player_location:
                is_matched+=1
    next_location = path_to_new_target.pop(0)
    UDRL=move_from_locations_step (player_location, next_location)

    return UDRL