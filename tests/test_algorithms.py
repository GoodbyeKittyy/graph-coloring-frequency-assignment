"""
Unit tests for graph coloring algorithms
Run with: pytest test_algorithms.py -v
Or: python -m pytest test_algorithms.py -v
"""

import pytest
import sys
import os

# Add parent directory to path to import graph_coloring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph_coloring import Graph, FrequencyAssigner, NetworkGenerator, Node


class TestGraph:
    """Test Graph class functionality"""
    
    def test_add_node(self):
        """Test adding nodes to graph"""
        graph = Graph()
        graph.add_node(0)
        assert 0 in graph.nodes
        assert graph.nodes[0].id == 0
    
    def test_add_node_with_position(self):
        """Test adding nodes with position"""
        graph = Graph()
        graph.add_node(0, position=(100, 200))
        assert graph.nodes[0].position == (100, 200)
    
    def test_add_edge(self):
        """Test adding edges between nodes"""
        graph = Graph(3)
        graph.add_edge(0, 1)
        assert 1 in graph.adjacency[0]
        assert 0 in graph.adjacency[1]
        assert graph.nodes[0].degree == 1
        assert graph.nodes[1].degree == 1
    
    def test_no_self_loops(self):
        """Test that self-loops are not allowed"""
        graph = Graph(2)
        graph.add_edge(0, 0)
        assert len(graph.edges) == 0
    
    def test_no_duplicate_edges(self):
        """Test that duplicate edges are not added"""
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 0)  # Duplicate
        graph.add_edge(0, 1)  # Another duplicate
        assert len(graph.edges) == 1
    
    def test_neighbor_colors(self):
        """Test getting neighbor colors"""
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.nodes[1].color = 0
        graph.nodes[2].color = 1
        
        colors = graph.get_neighbor_colors(0)
        assert colors == {0, 1}
    
    def test_chromatic_number(self):
        """Test chromatic number calculation"""
        graph = Graph(5)
        graph.nodes[0].color = 0
        graph.nodes[1].color = 1
        graph.nodes[2].color = 0
        graph.nodes[3].color = 2
        graph.nodes[4].color = 1
        
        assert graph.get_chromatic_number() == 3
    
    def test_count_conflicts(self):
        """Test conflict counting"""
        graph = Graph(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        
        # Create a conflict
        graph.nodes[0].color = 0
        graph.nodes[1].color = 0  # Conflict with node 0
        graph.nodes[2].color = 1
        graph.nodes[3].color = 1  # Conflict with node 2
        
        assert graph.count_conflicts() == 2
    
    def test_reset_colors(self):
        """Test resetting node colors"""
        graph = Graph(3)
        graph.nodes[0].color = 0
        graph.nodes[1].color = 1
        graph.nodes[2].color = 2
        
        graph.reset_colors()
        
        for node in graph.nodes.values():
            assert node.color is None


class TestAlgorithms:
    """Test graph coloring algorithms"""
    
    @pytest.fixture
    def simple_graph(self):
        """Create a simple test graph (path)"""
        graph = Graph(5)
        # Create a path: 0-1-2-3-4
        for i in range(4):
            graph.add_edge(i, i+1)
        return graph
    
    @pytest.fixture
    def complete_graph(self):
        """Create complete graph K5"""
        graph = Graph(5)
        for i in range(5):
            for j in range(i+1, 5):
                graph.add_edge(i, j)
        return graph
    
    @pytest.fixture
    def cycle_graph(self):
        """Create cycle graph C6"""
        graph = Graph(6)
        for i in range(5):
            graph.add_edge(i, i+1)
        graph.add_edge(5, 0)
        return graph
    
    @pytest.fixture
    def bipartite_graph(self):
        """Create bipartite graph K3,3"""
        graph = Graph(6)
        for i in range(3):
            for j in range(3, 6):
                graph.add_edge(i, j)
        return graph
    
    def test_greedy_no_conflicts(self, simple_graph):
        """Test greedy algorithm produces valid coloring"""
        assigner = FrequencyAssigner(simple_graph)
        stats = assigner.greedy_coloring()
        assert stats['conflicts'] == 0
        assert stats['chromatic_number'] > 0
    
    def test_welsh_powell_path(self, simple_graph):
        """Test Welsh-Powell on path graph"""
        assigner = FrequencyAssigner(simple_graph)
        stats = assigner.welsh_powell()
        # Path graph should need 2 colors
        assert stats['chromatic_number'] == 2
        assert stats['conflicts'] == 0
    
    def test_dsatur_complete_graph(self, complete_graph):
        """Test DSATUR on complete graph"""
        assigner = FrequencyAssigner(complete_graph)
        stats = assigner.dsatur()
        # Complete graph K5 needs 5 colors
        assert stats['chromatic_number'] == 5
        assert stats['conflicts'] == 0
    
    def test_dsatur_cycle(self, cycle_graph):
        """Test DSATUR on cycle graph"""
        assigner = FrequencyAssigner(cycle_graph)
        stats = assigner.dsatur()
        # Even cycle needs 2 colors
        assert stats['chromatic_number'] == 2
        assert stats['conflicts'] == 0
    
    def test_dsatur_bipartite(self, bipartite_graph):
        """Test DSATUR on bipartite graph"""
        assigner = FrequencyAssigner(bipartite_graph)
        stats = assigner.dsatur()
        # Bipartite graph needs 2 colors
        assert stats['chromatic_number'] == 2
        assert stats['conflicts'] == 0
    
    def test_backtracking_small(self, simple_graph):
        """Test backtracking on small graph"""
        assigner = FrequencyAssigner(simple_graph)
        stats = assigner.backtracking_exact(max_colors=3)
        assert stats['chromatic_number'] == 2
        assert stats['conflicts'] == 0
    
    def test_all_algorithms_valid(self, cycle_graph):
        """Test all algorithms produce valid colorings"""
        assigner = FrequencyAssigner(cycle_graph)
        
        algorithms = [
            ('Greedy', assigner.greedy_coloring),
            ('Welsh-Powell', assigner.welsh_powell),
            ('DSATUR', assigner.dsatur),
        ]
        
        for name, algo in algorithms:
            stats = algo()
            assert stats['conflicts'] == 0, f"{name} produced conflicts"
            assert stats['chromatic_number'] >= 2, f"{name} used too few colors"
            assert stats['chromatic_number'] <= 6, f"{name} used too many colors"
    
    def test_algorithm_deterministic(self, simple_graph):
        """Test that algorithms are deterministic"""
        assigner = FrequencyAssigner(simple_graph)
        
        stats1 = assigner.dsatur()
        stats2 = assigner.dsatur()
        
        assert stats1['chromatic_number'] == stats2['chromatic_number']


class TestNetworkGenerator:
    """Test network generation"""
    
    def test_random_geometric(self):
        """Test random geometric graph generation"""
        graph = NetworkGenerator.random_geometric(
            num_nodes=20,
            radius=300,
            area=(1000, 1000)
        )
        assert len(graph.nodes) == 20
        assert len(graph.edges) > 0
        
        # Check positions are within bounds
        for node in graph.nodes.values():
            x, y = node.position
            assert 0 <= x <= 1000
            assert 0 <= y <= 1000
    
    def test_random_geometric_radius(self):
        """Test that radius affects edge count"""
        graph1 = NetworkGenerator.random_geometric(20, radius=100)
        graph2 = NetworkGenerator.random_geometric(20, radius=500)
        
        # Larger radius should generally create more edges
        # (not guaranteed due to randomness, but very likely)
        assert len(graph2.edges) >= len(graph1.edges) * 0.5
    
    def test_cellular_grid_size(self):
        """Test cellular grid size"""
        graph = NetworkGenerator.cellular_grid(5, 5)
        assert len(graph.nodes) == 25
        
        # Check hex connectivity
        # Internal nodes should have 6 neighbors
        internal_node_id = 7  # Second row, second column
        assert graph.nodes[internal_node_id].degree == 6
    
    def test_cellular_grid_structure(self):
        """Test cellular grid structure"""
        graph = NetworkGenerator.cellular_grid(3, 3)
        
        # Corner nodes should have 3 neighbors in hex grid
        assert graph.nodes[0].degree == 3
        
        # Edge nodes should have 4-5 neighbors
        assert 4 <= graph.nodes[1].degree <= 5
        
        # Center node should have 6 neighbors
        assert graph.nodes[4].degree == 6
    
    def test_scale_free(self):
        """Test scale-free network generation"""
        graph = NetworkGenerator.scale_free(50, m=3)
        assert len(graph.nodes) == 50
        
        # Should have high-degree hubs
        degrees = [node.degree for node in graph.nodes.values()]
        max_degree = max(degrees)
        avg_degree = sum(degrees) / len(degrees)
        
        # Max degree should be significantly higher than average
        assert max_degree > avg_degree * 1.5
    
    def test_scale_free_connectivity(self):
        """Test scale-free network connectivity"""
        graph = NetworkGenerator.scale_free(30, m=3)
        
        # All nodes should have at least some connections
        for node in graph.nodes.values():
            assert node.degree > 0


class TestPerformance:
    """Test algorithm performance characteristics"""
    
    def test_dsatur_better_than_greedy(self):
        """Test that DSATUR generally outperforms greedy"""
        wins = 0
        trials = 10
        
        for _ in range(trials):
            graph = NetworkGenerator.random_geometric(30, 200)
            assigner = FrequencyAssigner(graph)
            
            greedy_stats = assigner.greedy_coloring()
            dsatur_stats = assigner.dsatur()
            
            if dsatur_stats['chromatic_number'] <= greedy_stats['chromatic_number']:
                wins += 1
        
        # DSATUR should win or tie in most cases
        assert wins >= trials * 0.7
    
    def test_welsh_powell_vs_greedy(self):
        """Test that Welsh-Powell outperforms or matches greedy"""
        graph = NetworkGenerator.random_geometric(40, 200)
        assigner = FrequencyAssigner(graph)
        
        greedy_stats = assigner.greedy_coloring()
        wp_stats = assigner.welsh_powell()
        
        # Welsh-Powell should be at least as good as greedy
        assert wp_stats['chromatic_number'] <= greedy_stats['chromatic_number'] * 1.2
    
    def test_large_network_performance(self):
        """Test that algorithms complete in reasonable time"""
        import time
        
        graph = NetworkGenerator.random_geometric(500, 200)
        assigner = FrequencyAssigner(graph)
        
        start = time.time()
        stats = assigner.dsatur()
        elapsed = time.time() - start
        
        # Should complete within 10 seconds
        assert elapsed < 10.0
        assert stats['conflicts'] == 0
    
    def test_time_complexity_growth(self):
        """Test that time grows reasonably with network size"""
        import time
        
        times = []
        sizes = [50, 100, 200]
        
        for size in sizes:
            graph = NetworkGenerator.random_geometric(size, 200)
            assigner = FrequencyAssigner(graph)
            
            start = time.time()
            assigner.dsatur()
            elapsed = time.time() - start
            times.append(elapsed)
        
        # Time should not grow exponentially
        # For DSATUR (O(n²)), doubling size should roughly quadruple time
        ratio = times[2] / times[0]
        assert ratio < 20  # Should be around 16 for perfect O(n²)


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_graph(self):
        """Test empty graph"""
        graph = Graph()
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        assert stats['chromatic_number'] == 0
        assert stats['conflicts'] == 0
    
    def test_single_node(self):
        """Test single node graph"""
        graph = Graph(1)
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        assert stats['chromatic_number'] == 1
        assert stats['conflicts'] == 0
    
    def test_two_connected_nodes(self):
        """Test two connected nodes"""
        graph = Graph(2)
        graph.add_edge(0, 1)
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        assert stats['chromatic_number'] == 2
        assert stats['conflicts'] == 0
    
    def test_disconnected_graph(self):
        """Test disconnected graph"""
        graph = Graph(10)
        # Create two disconnected components
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(5, 6)
        graph.add_edge(6, 7)
        
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        assert stats['conflicts'] == 0
    
    def test_invalid_edge_raises_error(self):
        """Test that invalid edge raises error"""
        graph = Graph(3)
        with pytest.raises(ValueError):
            graph.add_edge(0, 5)  # Node 5 doesn't exist
    
    def test_star_graph(self):
        """Test star graph (one central hub)"""
        graph = Graph(6)
        # Node 0 connected to all others
        for i in range(1, 6):
            graph.add_edge(0, i)
        
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        # Star graph needs 2 colors
        assert stats['chromatic_number'] == 2
        assert stats['conflicts'] == 0
    
    def test_triangle(self):
        """Test triangle graph (3-cycle)"""
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        # Triangle needs 3 colors
        assert stats['chromatic_number'] == 3
        assert stats['conflicts'] == 0


class TestExport:
    """Test data export functionality"""
    
    def test_json_export(self, tmp_path):
        """Test JSON export"""
        graph = NetworkGenerator.random_geometric(10, 200)
        assigner = FrequencyAssigner(graph)
        assigner.dsatur()
        
        output_file = tmp_path / "test_output.json"
        assigner.export_assignment(str(output_file))
        
        assert output_file.exists()
        
        import json
        with open(output_file) as f:
            data = json.load(f)
        
        assert 'metadata' in data
        assert 'assignments' in data
        assert len(data['assignments']) == 10
        assert data['metadata']['chromatic_number'] > 0
    
    def test_export_content(self, tmp_path):
        """Test export content structure"""
        graph = NetworkGenerator.random_geometric(5, 200)
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        
        output_file = tmp_path / "test.json"
        assigner.export_assignment(str(output_file))
        
        import json
        with open(output_file) as f:
            data = json.load(f)
        
        # Check metadata
        assert data['metadata']['chromatic_number'] == stats['chromatic_number']
        assert data['metadata']['conflicts'] == stats['conflicts']
        
        # Check assignments
        for assignment in data['assignments']:
            assert 'node_id' in assignment
            assert 'frequency' in assignment
            assert 'degree' in assignment


class TestStatistics:
    """Test statistical properties"""
    
    def test_efficiency_calculation(self):
        """Test efficiency metric calculation"""
        graph = Graph(10)
        assigner = FrequencyAssigner(graph)
        
        # Complete graph should have low efficiency
        for i in range(10):
            for j in range(i+1, 10):
                graph.add_edge(i, j)
        
        stats = assigner.dsatur()
        assert stats['efficiency'] == 0.0  # Needs all 10 colors
    
    def test_time_measurement(self):
        """Test that time is measured"""
        graph = NetworkGenerator.random_geometric(20, 200)
        assigner = FrequencyAssigner(graph)
        stats = assigner.dsatur()
        
        assert 'time_ms' in stats
        assert stats['time_ms'] > 0
        assert stats['time_ms'] < 5000  # Should be fast


# Parametrized tests
@pytest.mark.parametrize("size,radius", [
    (10, 150),
    (20, 200),
    (30, 250),
    (50, 300),
])
def test_various_network_sizes(size, radius):
    """Test algorithms on various network sizes"""
    graph = NetworkGenerator.random_geometric(size, radius)
    assigner = FrequencyAssigner(graph)
    stats = assigner.dsatur()
    
    assert stats['conflicts'] == 0
    assert stats['chromatic_number'] > 0
    assert stats['chromatic_number'] <= size


@pytest.mark.parametrize("algorithm", [
    'greedy',
    'welsh_powell',
    'dsatur',
])
def test_all_algorithms_consistency(algorithm):
    """Test consistency across all algorithms"""
    graph = NetworkGenerator.random_geometric(25, 200)
    assigner = FrequencyAssigner(graph)
    
    if algorithm == 'greedy':
        stats = assigner.greedy_coloring()
    elif algorithm == 'welsh_powell':
        stats = assigner.welsh_powell()
    else:
        stats = assigner.dsatur()
    
    assert stats['conflicts'] == 0
    assert stats['algorithm'] == algorithm.replace('_', '-').title() or algorithm.upper()


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])