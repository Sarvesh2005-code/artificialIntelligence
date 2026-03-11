import heapq 
 
def a_star(graph, start, goal, h): 
    pq = [(h[start], start)] 
    cost = {start: 0} 
    parent = {start: None} 
 
    while pq: 
        _, node = heapq.heappop(pq) 
 
        if node == goal: 
            path = [] 
            while node: 
                path.append(node) 
                node = parent[node] 
            return path[::-1] 
 
        for nxt, w in graph[node]: 
            new_cost = cost[node] + w 
            if nxt not in cost or new_cost < cost[nxt]: 
                cost[nxt] = new_cost 
                parent[nxt] = node 
                heapq.heappush(pq, (new_cost + h[nxt], nxt)) 
 
    return None 
# USER INPUT 
graph = {} 
heuristic = {} 
 
n = int(input("Enter number of nodes: ")) 
 
for _ in range(n): 
    node = input("Enter node name: ") 
    graph[node] = [] 
    heuristic[node] = int(input(f"Enter heuristic value for {node}: ")) 
 
e = int(input("Enter number of edges: ")) 
 
for _ in range(e): 
    u = input("From node: ") 
    v = input("To node: ") 
    w = int(input("Cost: ")) 
    graph[u].append((v, w)) 
 
start = input("Enter start node: ") 
goal = input("Enter goal node: ") 
 
path = a_star(graph, start, goal, heuristic) 
 
if path: 
    print("Optimal path:", path) 
else: 
    print("No path found") 