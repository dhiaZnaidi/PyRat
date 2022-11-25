def I_did_not_eat_that (metaGraph, eaten_pieces, pieces_of_cheese, player_location):
    
    if len(metaGraph) > len(pieces_of_cheese):
        for cheese in metaGraph :
            if cheese not in pieces_of_cheese and cheese != player_location:
                eaten_pieces.append(cheese)
    
    return eaten_pieces


def updatepieces (metaGraph, eaten_pieces, pieces_of_cheese):
    
    if len(metaGraph) > len(pieces_of_cheese):
        for cheese in metaGraph :
            if cheese not in pieces_of_cheese :
                eaten_pieces.append(cheese)
    
    return eaten_pieces




def metaGraphWithoutEaten (metaGraph, eaten_pieces):
    updated_meta_graph = {}

    
    for cheese in metaGraph.keys () : 
        if not a in eaten_pieces :
            updated_meta_graph[a] = {}
            for neighbour in metaGraph[cheese].keys () :
                if not b in eaten_pieces :
                    updated_meta_graph[cheese][neighbour] = metaGraph[cheese][neighbour]
                    
                    
    return updated_meta_graph
