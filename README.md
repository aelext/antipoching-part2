The Christofides algorithm is one of the most effective heuristic algorithms out there to tackle the Traveling Salesman Problem (TSP). Christofides algorithm guarantees a path that is at worst 1.5 times the optimum [1].

First, it creates a minimum spanning tree which is a tree that connects all the points in the graph with the smallest weight. Then it finds all of the odd vertices and perfectly pairs them together with the minimum weight. All the points can be paired together thanks to the handshaking lemma, which states that the amount of odd vertices in a graph will always be even. Then it combines the perfectly paired odd vertices and the MST into a multigraph so each vertex has an even degree which enables an Eulerian circuit to be formed, which is a circuit that visits every edge exactly once and ends on the same vertex. Then, using the circuit found in the previous step, it forms a Hamiltonian circuit by skipping repeated vertices, creating a graph that visits every vertex exactly once; a solution to the traveling salesman problem. The reason why the Christofides algorithm guarantees a path that is 1.5 times the optimal path is that the MST is always less than or equal to the optimal path, and perfectly matching the odd vertices gives a weight that can be no larger than half the optimal path. Adding these two weights gives the maximum weight of the Eulerian circuit, which is 1.5 times the optimal path, and shortcutting does not affect the weight at all, meaning that the path that the Christofides algorithm gives is always at worst 1.5 times the optimum.

Minimum spanning tree from Kruskal's Algorithm:
<img width="1099" alt="Screenshot 2025-04-14 at 18 42 10" src="https://github.com/user-attachments/assets/6b74064b-efa4-49e7-a94b-23bb35e6958a" />

Odd degree points:
<img width="1102" alt="Screenshot 2025-04-14 at 18 42 41" src="https://github.com/user-attachments/assets/b54ab0c5-1cfa-4014-ac5e-65574112089e" />

Minimum weight perfect matching (Suboptimal due to usage of greedy algorithm):
<img width="1101" alt="Screenshot 2025-04-14 at 18 43 04" src="https://github.com/user-attachments/assets/8402d6d7-4fbb-4dd7-bf8d-c3da95335500" />

Eulerian Tour:
<img width="1098" alt="Screenshot 2025-04-14 at 18 44 09" src="https://github.com/user-attachments/assets/0c6b524a-4943-4ccd-a0f9-ab761d49c017" />

Output following the construction of the Hamiltonian Circuit
<img width="1097" alt="Screenshot 2025-04-14 at 18 44 33" src="https://github.com/user-attachments/assets/f87fd5eb-9288-4a1b-a3bd-f46059d3eaf5" />

Output following pairing with the 2-opt algorithm
<img width="1098" alt="Screenshot 2025-04-14 at 18 46 38" src="https://github.com/user-attachments/assets/10828d92-a978-4bad-aae3-bee37707e210" />
Final Distance: 46.947 kilometers
