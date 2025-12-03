"""
Advanced Graph Coloring for Network Frequency Assignment
Industrial-grade implementation with multiple algorithms
"""

import numpy as np
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
import json
import time
from collections import defaultdict, deque


@dataclass
class Node:
    """Represents a network node (cell tower, IoT device, etc.)"""
    id: int
    position: Tuple[float, float] = (0.0, 0.0)
    color: Optional[int] = None
    degree: int = 0
    saturation: int = 0
    neighbors: Set[int] = None
    
    def __post_init__(self):
        if self.neighbors is None:
            self.neighbors = set()


class Graph:
    """Graph representation for frequency assignment network"""
    
    def __init__(self, num_nodes: int = 0):
        self.nodes: Dict[int, Node] = {}
        self.edges: List[Tuple[int, int]] = []
        self.adjacency: Dict[int, Set[int]] = defaultdict(set)
        
        for i in range(num_nodes):
            self.add_node(i)
    
    def add_node(self, node_id: int, position: Tuple[float, float] = (0.0, 0.0)):
        """Add a node to the graph"""
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(id=node_id, position=position)
    
    def add_edge(self, u: int, v: int):
        """Add an edge (interference link) between two nodes"""
        if u not in self.nodes or v not in self.nodes:
            raise ValueError(f"Nodes {u} or {v} not in graph")
        
        if u != v and v not in self.adjacency[u]:
            self.edges.append((u, v))
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)
            self.nodes[u].degree += 1
            self.nodes[v].degree += 1
            self.nodes[u].neighbors.add(v)
            self.nodes[v].neighbors.add(u)
    
    def get_neighbor_colors(self, node_id: int) -> Set[int]:
        """Get all colors used by neighbors of a node"""
        colors = set()
        for neighbor in self.adjacency[node_id]:
            if self.nodes[neighbor].color is not None:
                colors.add(self.nodes[neighbor].color)
        return colors
    
    def get_chromatic_number(self) -> int:
        """Return the number of colors used"""
        colors = {node.color for node in self.nodes.values() if node.color is not None}
        return len(colors)
    
    def count_conflicts(self) -> int:
        """Count the number of edges with same-colored endpoints"""
        conflicts = 0
        for u, v in self.edges:
            if (self.nodes[u].color is not None and 
                self.nodes[v].color is not None and
                self.nodes[u].color == self.nodes[v].color):
                conflicts += 1
        return conflicts
    
    def reset_colors(self):
        """Reset all node colors"""
        for node in self.nodes.values():
            node.color = None
            node.saturation = 0


class FrequencyAssigner:
    """Main class for frequency assignment using graph coloring"""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.stats = {
            'algorithm': '',
            'chromatic_number': 0,
            'conflicts': 0,
            'time_ms': 0,
            'efficiency': 0.0
        }
    
    def get_smallest_available_color(self, neighbor_colors: Set[int]) -> int:
        """Find the smallest color not used by neighbors"""
        color = 0
        while color in neighbor_colors:
            color += 1
        return color
    
    def greedy_coloring(self) -> Dict[str, any]:
        """Basic greedy coloring algorithm"""
        start_time = time.time()
        self.graph.reset_colors()
        
        for node_id in sorted(self.graph.nodes.keys()):
            neighbor_colors = self.graph.get_neighbor_colors(node_id)
            self.graph.nodes[node_id].color = self.get_smallest_available_color(neighbor_colors)
        
        return self._compute_stats('Greedy', time.time() - start_time)
    
    def welsh_powell(self) -> Dict[str, any]:
        """Welsh-Powell algorithm: color nodes in decreasing order of degree"""
        start_time = time.time()
        self.graph.reset_colors()
        
        # Sort nodes by degree (descending)
        sorted_nodes = sorted(
            self.graph.nodes.values(),
            key=lambda n: n.degree,
            reverse=True
        )
        
        for node in sorted_nodes:
            neighbor_colors = self.graph.get_neighbor_colors(node.id)
            node.color = self.get_smallest_available_color(neighbor_colors)
        
        return self._compute_stats('Welsh-Powell', time.time() - start_time)
    
    def dsatur(self) -> Dict[str, any]:
        """
        DSATUR algorithm (Degree of Saturation)
        Superior performance - prioritizes nodes with most colored neighbors
        """
        start_time = time.time()
        self.graph.reset_colors()
        
        uncolored = set(self.graph.nodes.keys())
        
        # Color the node with highest degree first
        if uncolored:
            first_node = max(uncolored, key=lambda n: self.graph.nodes[n].degree)
            self.graph.nodes[first_node].color = 0
            uncolored.remove(first_node)
            
            # Update saturation for neighbors
            for neighbor in self.graph.adjacency[first_node]:
                if neighbor in uncolored:
                    self.graph.nodes[neighbor].saturation += 1
        
        # Color remaining nodes
        while uncolored:
            # Select node with highest saturation (tie-break by degree)
            selected = max(
                uncolored,
                key=lambda n: (
                    self.graph.nodes[n].saturation,
                    self.graph.nodes[n].degree
                )
            )
            
            node = self.graph.nodes[selected]
            neighbor_colors = self.graph.get_neighbor_colors(selected)
            node.color = self.get_smallest_available_color(neighbor_colors)
            uncolored.remove(selected)
            
            # Update saturation for uncolored neighbors
            for neighbor in self.graph.adjacency[selected]:
                if neighbor in uncolored:
                    neighbor_colors = self.graph.get_neighbor_colors(neighbor)
                    self.graph.nodes[neighbor].saturation = len(neighbor_colors)
        
        return self._compute_stats('DSATUR', time.time() - start_time)
    
    def backtracking_exact(self, max_colors: int = None) -> Dict[str, any]:
        """
        Exact backtracking algorithm (exponential time)
        Only for small graphs (<50 nodes)
        """
        start_time = time.time()
        self.graph.reset_colors()
        
        if max_colors is None:
            max_colors = len(self.graph.nodes)
        
        node_ids = list(self.graph.nodes.keys())
        
        def backtrack(idx: int) -> bool:
            if idx == len(node_ids):
                return True
            
            node_id = node_ids[idx]
            neighbor_colors = self.graph.get_neighbor_colors(node_id)
            
            for color in range(max_colors):
                if color not in neighbor_colors:
                    self.graph.nodes[node_id].color = color
                    if backtrack(idx + 1):
                        return True
                    self.graph.nodes[node_id].color = None
            
            return False
        
        success = backtrack(0)
        if not success:
            return {'error': 'No solution found with given color limit'}
        
        return self._compute_stats('Backtracking-Exact', time.time() - start_time)
    
    def largest_first(self) -> Dict[str, any]:
        """
        Largest First algorithm: similar to Welsh-Powell
        Colors nodes in order of decreasing degree
        """
        return self.welsh_powell()
    
    def _compute_stats(self, algorithm: str, elapsed_time: float) -> Dict[str, any]:
        """Compute and return statistics"""
        chromatic = self.graph.get_chromatic_number()
        conflicts = self.graph.count_conflicts()
        num_nodes = len(self.graph.nodes)
        
        # Efficiency: how well we minimize frequencies
        efficiency = ((num_nodes - chromatic) / num_nodes * 100) if num_nodes > 0 else 0
        
        self.stats = {
            'algorithm': algorithm,
            'chromatic_number': chromatic,
            'conflicts': conflicts,
            'time_ms': round(elapsed_time * 1000, 2),
            'efficiency': round(efficiency, 2),
            'nodes': num_nodes,
            'edges': len(self.graph.edges)
        }
        
        return self.stats
    
    def export_assignment(self, filename: str):
        """Export frequency assignments to JSON"""
        assignments = {
            'metadata': self.stats,
            'assignments': [
                {
                    'node_id': node.id,
                    'frequency': node.color,
                    'position': node.position,
                    'degree': node.degree
                }
                for node in self.graph.nodes.values()
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(assignments, f, indent=2)
        
        print(f"✓ Assignment exported to {filename}")


class NetworkGenerator:
    """Generate realistic network topologies for testing"""
    
    @staticmethod
    def random_geometric(num_nodes: int, radius: float, 
                        area: Tuple[float, float] = (1000, 1000)) -> Graph:
        """
        Generate random geometric graph
        Nodes connect if within interference radius
        """
        graph = Graph()
        
        # Generate random positions
        positions = np.random.rand(num_nodes, 2) * np.array(area)
        
        for i in range(num_nodes):
            graph.add_node(i, tuple(positions[i]))
        
        # Add edges based on distance
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist <= radius:
                    graph.add_edge(i, j)
        
        return graph
    
    @staticmethod
    def cellular_grid(rows: int, cols: int, 
                      connectivity: str = 'hex') -> Graph:
        """
        Generate cellular network grid
        connectivity: 'square' or 'hex'
        """
        graph = Graph()
        num_nodes = rows * cols
        
        for i in range(rows):
            for j in range(cols):
                node_id = i * cols + j
                graph.add_node(node_id, (j * 100, i * 100))
        
        # Add edges based on connectivity
        for i in range(rows):
            for j in range(cols):
                node_id = i * cols + j
                
                # Right neighbor
                if j < cols - 1:
                    graph.add_edge(node_id, node_id + 1)
                
                # Bottom neighbor
                if i < rows - 1:
                    graph.add_edge(node_id, node_id + cols)
                
                if connectivity == 'hex':
                    # Diagonal neighbors for hex pattern
                    if i < rows - 1 and j > 0:
                        graph.add_edge(node_id, node_id + cols - 1)
                    if i < rows - 1 and j < cols - 1:
                        graph.add_edge(node_id, node_id + cols + 1)
        
        return graph
    
    @staticmethod
    def scale_free(num_nodes: int, m: int = 3) -> Graph:
        """
        Generate scale-free network (Barabási-Albert model)
        Realistic for IoT deployments
        """
        graph = Graph()
        
        # Start with m nodes
        for i in range(m):
            graph.add_node(i)
        
        for i in range(m - 1):
            for j in range(i + 1, m):
                graph.add_edge(i, j)
        
        # Add remaining nodes with preferential attachment
        for i in range(m, num_nodes):
            graph.add_node(i)
            
            # Calculate attachment probabilities
            degrees = [graph.nodes[j].degree for j in range(i)]
            total_degree = sum(degrees)
            
            if total_degree == 0:
                probs = [1/i] * i
            else:
                probs = [d / total_degree for d in degrees]
            
            # Attach to m existing nodes
            targets = np.random.choice(i, size=min(m, i), replace=False, p=probs)
            for target in targets:
                graph.add_edge(i, int(target))
        
        return graph


def compare_algorithms(graph: Graph) -> pd.DataFrame:
    """Compare all algorithms on the same graph"""
    import pandas as pd
    
    assigner = FrequencyAssigner(graph)
    results = []
    
    algorithms = [
        ('Greedy', assigner.greedy_coloring),
        ('Welsh-Powell', assigner.welsh_powell),
        ('DSATUR', assigner.dsatur),
    ]
    
    # Add exact algorithm only for small graphs
    if len(graph.nodes) <= 30:
        algorithms.append(('Backtracking', assigner.backtracking_exact))
    
    for name, algo in algorithms:
        stats = algo()
        results.append(stats)
    
    return pd.DataFrame(results)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("ADVANCED NETWORK FREQUENCY ASSIGNMENT SYSTEM")
    print("=" * 60)
    
    # Generate a realistic network
    print("\n1. Generating random geometric network (cellular towers)...")
    graph = NetworkGenerator.random_geometric(
        num_nodes=50,
        radius=250,
        area=(1000, 1000)
    )
    print(f"   ✓ Generated {len(graph.nodes)} nodes, {len(graph.edges)} interference links")
    
    # Test DSATUR algorithm (best performance)
    print("\n2. Running DSATUR algorithm...")
    assigner = FrequencyAssigner(graph)
    stats = assigner.dsatur()
    
    print(f"\n   RESULTS:")
    print(f"   • Frequencies used: {stats['chromatic_number']}")
    print(f"   • Conflicts: {stats['conflicts']}")
    print(f"   • Efficiency: {stats['efficiency']}%")
    print(f"   • Computation time: {stats['time_ms']} ms")
    
    # Export results
    print("\n3. Exporting assignments...")
    assigner.export_assignment('frequency_assignment.json')
    
    # Compare algorithms
    print("\n4. Comparing all algorithms...")
    try:
        import pandas as pd
        comparison = compare_algorithms(graph)
        print("\n", comparison.to_string(index=False))
    except ImportError:
        print("   Install pandas for algorithm comparison: pip install pandas")
    
    print("\n" + "=" * 60)
    print("✓ Analysis complete!")
    print("=" * 60)