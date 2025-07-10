#################################################
# Name:        Keenan Grant                     #
# Date:         1/16/2025                       #
# Class:        CPSC 4420                       #
# Assignment:   Final Project                   #
#################################################

import networkx as nx
import matplotlib.pyplot as plt
import heapq

S3B2_distance = 0
travel_node_pos = {"Start": (740 + S3B2_distance, 384),
                            "E1B1": (984, 960), "E1B2": (984, 576),
                            "E2B1": (1688, 960), "E2B2": (1688, 384),
                            "S1B1": (804, 960), "S1B2": (1008, 768),
                            "S2B1": (1316, 768), "S2B2": (1516, 576),
                            "S3B1": (936, 576), "S3B2": (740, 384),
                            "Desk": (588, 768), "Washer1": (908, 768), "Washer2": (964, 768), "Arcade": (1036, 768), "Arcade Hide": (1164, 768), "Bathroom Sink": (1600, 768),
                            "Door Dresser": (584, 960), "StairSafe": (872, 960), "Fireplace": (1104, 960), "Left Table": (1288, 960), "Kitchen Cabinet": (1480, 960)}

def a_star_algorithm(graph, start, goal, heuristic_fn):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic_fn(start, goal)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_fn(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def heuristic_function(node, goal):
    """Calculates the heuristic as the Manhattan distance to the goal."""
    node_pos = travel_node_pos[node]
    goal_pos = travel_node_pos[goal]  # Use the destination position as the goal

    if goal == "Bathroom Sink":
        return 0
    else:
        return abs(node_pos[0] - goal_pos[0]) + abs(node_pos[1] - goal_pos[1])

def main():
    # global S3B2_distance, E2B2_distance
    graph = nx.Graph()

    # Hardcoded nodes and edges
    nodes = ['Start', 'S3B2', 'E2B2', 'S3B1', 'E1B2', 'S2B2', 'S2B1', 'S1B2', 'S1B1', 'E1B1', 'E2B1']
    goal_nodes = ['Desk', 'Washer1', 'Washer2', 'Arcade', 'Arcade Hide', 'Bathroom Sink',
                  'Door Dresser', 'StairSafe', 'Fireplace', 'Left Table', 'Kitchen Cabinet']
    edges = [
        # Distance (in pixels) costs
        # ('Start', 'S3B2', 0), ('Start', 'E2B2', 0), ('E2B2', 'E2B1', 576), ('S3B2', 'S3B1', 269), ('S3B1', 'E1B2', 48), ('E1B2', 'E1B1', 388), ('E1B2', 'S2B2', 532), ('S2B2', 'S2B1', 269), ('S2B1', 'S1B2', 312), ('S1B2', 'S1B1', 269), ('S1B1', 'E1B1', 180), ('E1B1', 'E2B1', 704),
        # ('S1B2', 'Desk', 420), ('S1B2', 'Washer1', 100), ('S1B2', 'Washer2', 44), ('S1B2', 'Arcade', 28), ('S1B2', 'Arcade Hide', 156), ('S1B2', 'Bathroom Sink', 592),
        # ('S2B1', 'Desk', 728), ('S2B1', 'Washer1', 408), ('S2B1', 'Washer2', 352), ('S2B1', 'Arcade', 280), ('S2B1', 'Arcade Hide', 152), ('S2B1', 'Bathroom Sink', 284),
        # ('S1B1', 'Door Dresser', 220), ('S1B1', 'StairSafe', 68), ('S1B1', 'Fireplace', 300), ('S1B1', 'Left Table', 484), ('S1B1', 'Kitchen Cabinet', 676),
        # ('E1B1', 'Door Dresser', 397), ('E1B1', 'StairSafe', 112), ('E1B1', 'Fireplace', 125), ('E1B1', 'Left Table', 304), ('E1B1', 'Kitchen Cabinet', 496),
        # ('E2B1', 'Door Dresser', 1104), ('E2B1', 'StairSafe', 816), ('E2B1', 'Fireplace', 584), ('E2B1', 'Left Table', 400), ('E2B1', 'Kitchen Cabinet', 208)]
    
        # Time (in seconds) costs
        ('Start', 'S3B2', 0), ('Start', 'E2B2', 0), ('E2B2', 'E2B1', 9.6), ('S3B2', 'S3B1', 2.69), ('S3B1', 'E1B2', 0.48), ('E1B2', 'E1B1', 6.47), ('E1B2', 'S2B2', 5.32), ('S2B2', 'S2B1', 2.69), ('S2B1', 'S1B2', 3.12), ('S1B2', 'S1B1', 2.69), ('S1B1', 'E1B1', 1.8), ('E1B1', 'E2B1', 11.73),
        ('S1B2', 'Desk', 4.2), ('S1B2', 'Washer1', 1), ('S1B2', 'Washer2', 0.44), ('S1B2', 'Arcade', 0.28), ('S1B2', 'Arcade Hide', 1.56), ('S1B2', 'Bathroom Sink', 5.92),
        ('S2B1', 'Desk', 7.28), ('S2B1', 'Washer1', 4.08), ('S2B1', 'Washer2', 3.52), ('S2B1', 'Arcade', 2.8), ('S2B1', 'Arcade Hide', 1.52), ('S2B1', 'Bathroom Sink', 2.84),
        ('S1B1', 'Door Dresser', 2.2), ('S1B1', 'StairSafe', 0.68), ('S1B1', 'Fireplace', 3), ('S1B1', 'Left Table', 4.84), ('S1B1', 'Kitchen Cabinet', 6.76),
        ('E1B1', 'Door Dresser', 3.97), ('E1B1', 'StairSafe', 1.12), ('E1B1', 'Fireplace', 1.25), ('E1B1', 'Left Table', 3.04), ('E1B1', 'Kitchen Cabinet', 4.96),
        ('E2B1', 'Door Dresser', 11.04), ('E2B1', 'StairSafe', 8.16), ('E2B1', 'Fireplace', 5.84), ('E2B1', 'Left Table', 4), ('E2B1', 'Kitchen Cabinet', 2.08)]

    for node in nodes:
        graph.add_node(node)

    print("Enter edge costs for 'S3B2' and 'E2B2':")
    while True:
        try:
            S3B2_distance = int(input("Enter cost from 'Start' to 'S3B2': "))
            e2b2_cost = int(input("Enter cost from 'Start' to 'E2B2': "))
            edges[0] = ('Start', 'S3B2', S3B2_distance / 100)
            edges[1] = ('Start', 'E2B2', e2b2_cost / 100)
            break
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    for edge in edges:
        graph.add_edge(edge[0], edge[1], weight=edge[2])

    start = 'Start'  # Hardcoded start node

    print("Available goal nodes:")
    for goal in goal_nodes:
        print(f"- {goal}")

    while True:
        goal = input("Enter the goal node by name: ").strip()
        if goal in goal_nodes:
            break
        else:
            print("Invalid selection. Please enter a valid goal node.")

    path = a_star_algorithm(graph, start, goal, heuristic_function)

    if path:
        print(f"Shortest path: {' -> '.join(path)}")
    else:
        print("No path found.")

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)})
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.show()

if __name__ == "__main__":
    main()