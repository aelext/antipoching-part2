# %%
import folium
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
from collections import defaultdict

# %%
class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

# %%
points = []
points.clear()
csv = pd.read_csv("Coordinates.csv")
for index, row in csv.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    points.append(Point(latitude, longitude))

# %%
def distance(point1, point2):
    return geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).kilometers

# %%
def totalDistance(order):
    totalDistance = 0
    numPoints = len(order)
    for i in range(numPoints - 1):
        point1 = order[i]
        point2 = order[i + 1]
        distance1 = distance(point1, point2)
        totalDistance += distance1
    return totalDistance

# %%
numPoints = len(points)
graph = [[0] * numPoints for _ in range(numPoints)]
for i in range(numPoints):
    for j in range(i + 1, numPoints):
        dist = distance(points[i], points[j])
        graph[i][j] = graph[j][i] = dist
parent = list(range(numPoints))
print(parent)

# %%
#Find MST via Kruskal's Algorithm
def kruskalMST(graph, points):
    numPoints = len(points)
    edges = []
    for i in range(numPoints):
        for j in range(i + 1, numPoints):
            if graph[i][j] > 0:
                edges.append((i, j, graph[i][j]))
    edges.sort(key = lambda edge: edge[2])
    for i in range(numPoints):
        parent[i] = i
        mst = []
    for edge in edges:
        u, v, weight = edge
        parent_u = u
        parent_v = v
        
        
        while parent[parent_u] != parent_u:
            parent_u = parent[parent_u]
        while parent[parent_v] != parent_v:
            parent_v = parent[parent_v]
        
        if parent_u != parent_v:  # Adding the edge doesn't create a cycle
            mst.append(edge)
            parent[parent_u] = parent_v
        
        if len(mst) == numPoints - 1:
            break
    return mst
mst = kruskalMST(graph, points)
print(mst)
print(len(mst))

# %%
Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)

# %%
for edge in mst:
    u, v, weight = edge
    folium.PolyLine([(points[u].latitude, points[u].longitude), (points[v].latitude, points[v].longitude)],
                    color='blue', weight=2.5, opacity=1).add_to(Map)
count = 0
for point in points:
    folium.Marker(location = [point.latitude, point.longitude], 
                  popup = [point.latitude, point.longitude, count], 
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
    count+=1
folium.Marker(location = [points[0].latitude, points[0].longitude], 
                  popup = [points[0].latitude, points[0].longitude, 0], 
                  icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)
Map

# %%
def oddDegreeNodes(mst):
    degrees = defaultdict(int)

    for fromNode, toNode, weight in mst:
        degrees[fromNode] += 1
        degrees[toNode] += 1

    oddNodes = set()
    for node, degree in degrees.items():
        if degree % 2 == 1:
            oddNodes.add(node)

    return oddNodes

# %%
oddNodes = oddDegreeNodes(mst)
print("Points with Odd Degree:", oddNodes)
print(len(oddNodes))

# %%
Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)
for point in oddNodes:
    folium.Marker(location = [points[point].latitude, points[point].longitude], 
                  popup = [points[point].latitude, points[point].longitude], 
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
Map

# %%
#Perfect match by linking the shortest distances between the odd nodes; suboptimal but works
#stuck here for a while due to lack of intuitive algorithm's for perfect matching
def greedyPerfectMatching(oddNodes, points):
    edges = []
    
    for i in oddNodes:
        for j in oddNodes:
            if i < j:
                dist = distance(points[i], points[j])
                edges.append((i, j, dist))
    
    # Sort edges by distance
    edges.sort(key=lambda x: x[2])
    
    matched = []
    matching = []
    
    for edge in edges:
        u, v, dist = edge
        if u not in matched and v not in matched:
            matching.append(edge)
            matched.append(u)
            matched.append(v)
    
    return matching
matched = greedyPerfectMatching(oddNodes, points)
print(matched)


Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)

for edge in matched:
    u, v, weight = edge
    folium.PolyLine([(points[u].latitude, points[u].longitude), (points[v].latitude, points[v].longitude)],
                    color='blue', weight=2.5, opacity=1).add_to(Map)
for i in oddNodes:
    folium.Marker(location=[points[i].latitude, points[i].longitude],
                  popup=[points[i].latitude, points[i].longitude],
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
Map

# %%
#Create eulerian tour with Hierholzer's Algorithm
def createEulerianTour(multigraph, numPoints):
    graph = defaultdict(list)
    for u, v, weight in multigraph:
        graph[u].append(v)
        graph[v].append(u)
    
    #startVertex = 0
    #for u in range(numPoints):
    #    if graph[u]:
    #        startVertex = u
    #        break
    
    #if startVertex is None:
    #    return []
    
    currPath = [0]
    path = []
    
    while currPath:
        u = currPath[-1]
        if graph[u]:
            v = graph[u].pop()
            graph[v].remove(u)
            currPath.append(v)
        else:
            path.append(currPath.pop())
        
    return path[::-1]

# Create the multigraph with MST and perfect matching
multigraph = mst.copy()
for u, v, weight in matched:
    multigraph.append((u, v, weight))

eulerianTour = createEulerianTour(multigraph, numPoints)
print("Eulerian Tour:", eulerianTour)
print(len(eulerianTour))

Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)

for i in range(len(eulerianTour) - 1):
    u = eulerianTour[i]
    v = eulerianTour[i + 1]
    folium.PolyLine([(points[u].latitude, points[u].longitude), (points[v].latitude, points[v].longitude)],
                    color='blue', weight=2.5, opacity=1).add_to(Map)
count = 0
for point in points:
    folium.Marker(location=[point.latitude, point.longitude],
                  popup=[point.latitude, point.longitude, count],
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
    count+=1

folium.Marker(location=[points[0].latitude, points[0].longitude],
              popup=[points[0].latitude, points[0].longitude],
              icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)

Map

# %%
# Shortcut the eulerian circuit and creating a hamiltonion circuit
def createHamiltonionCircuit(eulerianTour):
    visited = []
    hamiltonionCircuit = []
    for v in eulerianTour:
        if v not in visited:
            visited.append(v)
            hamiltonionCircuit.append(v)
    hamiltonionCircuit.append(hamiltonionCircuit[0]) #don't forget last point
    return hamiltonionCircuit

hamiltonionCircuit = createHamiltonionCircuit(eulerianTour)
print("Hamiltonion Circuit: ", hamiltonionCircuit)


Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)

for i in range(len(hamiltonionCircuit) - 1):
    u = hamiltonionCircuit[i]
    v = hamiltonionCircuit[i + 1]
    folium.PolyLine([(points[u].latitude, points[u].longitude), (points[v].latitude, points[v].longitude)],
                    color='blue', weight=2.5, opacity=1).add_to(Map)
count = 0
for point in points:
    folium.Marker(location=[point.latitude, point.longitude],
                  popup=[point.latitude, point.longitude, count],
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
    count+=1

folium.Marker(location=[points[0].latitude, points[0].longitude],
              popup=[points[0].latitude, points[0].longitude],
              icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)

Map

# %%


