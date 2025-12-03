"""
Basic usage examples for the graph coloring library
"""

import sys
sys.path.insert(0, '..')

from graph_coloring import Graph, FrequencyAssigner, NetworkGenerator


def example_1_simple_network():
    """Example 1: Create and color a simple network"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Network")
    print("="*60)
    
    # Create a simple graph with 10 nodes
    graph = Graph(10)
    
    # Add some interference relationships
    edges = [(0,1), (1,2), (2,3), (3,4), (4,5), 
             (0,3), (1,4), (2,5), (6,7), (7,8), (8,9)]
    
    for u, v in edges:
        graph.add_edge(u, v)
    
    print(f"Created network with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    
    # Assign frequencies using DSATUR
    assigner = FrequencyAssigner(graph)
    stats = assigner.dsatur()
    
    print(f"\nResults:")
    print(f"  Frequencies needed: {stats['chromatic_number']}")
    print(f"  Conflicts: {stats['conflicts']}")
    print(f"  Computation time: {stats['time_ms']:.2f} ms")
    
    # Print frequency assignments
    print(f"\nFrequency Assignments:")
    for node_id, node in graph.nodes.items():
        print(f"  Node {node_id}: Frequency {node.color}")


def example_2_cellular_network():
    """Example 2: Cellular tower frequency assignment"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Cellular Network (50 towers)")
    print("="*60)
    
    # Generate a realistic cellular network
    # 50 towers spread across 1km x 1km area
    # 250m interference radius
    graph = NetworkGenerator.random_geometric(
        num_nodes=50,
        radius=250,
        area=(1000, 1000)
    )
    
    print(f"Generated cellular network:")
    print(f"  Towers: {len(graph.nodes)}")
    print(f"  Interference links: {len(graph.edges)}")
    
    # Compare algorithms
    assigner = FrequencyAssigner(graph)
    
    print("\nAlgorithm Comparison:")
    print("-" * 60)
    
    # Greedy
    stats_greedy = assigner.greedy_coloring()
    print(f"Greedy:        {stats_greedy['chromatic_number']} frequencies, "
          f"{stats_greedy['time_ms']:.2f} ms")
    
    # Welsh-Powell
    stats_wp = assigner.welsh_powell()
    print(f"Welsh-Powell:  {stats_wp['chromatic_number']} frequencies, "
          f"{stats_wp['time_ms']:.2f} ms")
    
    # DSATUR (best)
    stats_dsatur = assigner.dsatur()
    print(f"DSATUR:        {stats_dsatur['chromatic_number']} frequencies, "
          f"{stats_dsatur['time_ms']:.2f} ms (BEST)")
    
    # Export results
    assigner.export_assignment('cellular_network_result.json')


def example_3_iot_network():
    """Example 3: IoT sensor network with scale-free topology"""
    print("\n" + "="*60)
    print("EXAMPLE 3: IoT Sensor Network (100 devices)")
    print("="*60)
    
    # Generate scale-free network (realistic for IoT)
    graph = NetworkGenerator.scale_free(num_nodes=100, m=4)
    
    print(f"Generated IoT network:")
    print(f"  Devices: {len(graph.nodes)}")
    print(f"  Communication links: {len(graph.edges)}")
    
    # Calculate network statistics
    degrees = [node.degree for node in graph.nodes.values()]
    avg_degree = sum(degrees) / len(degrees)
    max_degree = max(degrees)
    
    print(f"  Average degree: {avg_degree:.1f}")
    print(f"  Max degree (hub): {max_degree}")
    
    # Assign channels
    assigner = FrequencyAssigner(graph)
    stats = assigner.dsatur()
    
    print(f"\nChannel Assignment:")
    print(f"  Channels needed: {stats['chromatic_number']}")
    print(f"  Spectrum efficiency: {stats['efficiency']:.1f}%")
    print(f"  Conflicts: {stats['conflicts']}")


def example_4_wifi_channels():
    """Example 4: WiFi access point channel assignment"""
    print("\n" + "="*60)
    print("EXAMPLE 4: WiFi Channel Assignment (Building)")
    print("="*60)
    
    # Create a grid representing a building with APs
    # 5x5 grid = 25 access points
    graph = NetworkGenerator.cellular_grid(rows=5, cols=5, connectivity='hex')
    
    print(f"Building configuration:")
    print(f"  Access points: {len(graph.nodes)}")
    print(f"  Interference relationships: {len(graph.edges)}")
    
    # Assign 2.4GHz WiFi channels (typically 3 non-overlapping: 1, 6, 11)
    assigner = FrequencyAssigner(graph)
    stats = assigner.dsatur()
    
    print(f"\nWiFi Channel Assignment:")
    print(f"  Channels required: {stats['chromatic_number']}")
    
    if stats['chromatic_number'] <= 3:
        print(f"  ✓ Can use standard 2.4GHz channels (1, 6, 11)")
    else:
        print(f"  ⚠ Need 5GHz channels or reduce AP density")
    
    # Show channel map
    print(f"\nChannel Map (grid layout):")
    channel_map = ['Ch.1', 'Ch.6', 'Ch.11', 'Ch.36', 'Ch.40']
    
    for i in range(5):
        row = []
        for j in range(5):
            node_id = i * 5 + j
            color = graph.nodes[node_id].color
            row.append(channel_map[color] if color < len(channel_map) else f'Ch.{color}')
        print(f"  {' | '.join(row)}")


def example_5_custom_constraints():
    """Example 5: Custom frequency constraints"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Constraints")
    print("="*60)
    
    # Create network
    graph = NetworkGenerator.random_geometric(30, 200)
    
    print(f"Network: {len(graph.nodes)} nodes")
    
    # Standard coloring
    assigner = FrequencyAssigner(graph)
    stats_normal = assigner.dsatur()
    
    print(f"\nWithout constraints:")
    print(f"  Frequencies: {stats_normal['chromatic_number']}")
    
    # Now with constraint: certain nodes must use specific frequencies
    # (e.g., legacy equipment that only supports certain frequencies)
    print(f"\nWith constraints:")
    print(f"  Nodes 0-4 pre-assigned to frequency 0 (legacy equipment)")
    
    # Pre-assign colors
    for i in range(5):
        graph.nodes[i].color = 0
    
    # Color remaining nodes
    for node_id in range(5, len(graph.nodes)):
        neighbor_colors = graph.get_neighbor_colors(node_id)
        color = 0
        while color in neighbor_colors:
            color += 1
        graph.nodes[node_id].color = color
    
    # Check results
    chromatic = graph.get_chromatic_number()
    conflicts = graph.count_conflicts()
    
    print(f"  Frequencies: {chromatic}")
    print(f"  Conflicts: {conflicts}")


def example_6_large_scale():
    """Example 6: Large-scale deployment (1000+ nodes)"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Large-Scale Deployment (1000 nodes)")
    print("="*60)
    
    print("Generating large network (this may take a moment)...")
    
    # Generate large network
    graph = NetworkGenerator.random_geometric(1000, 200)
    
    print(f"\nNetwork statistics:")
    print(f"  Nodes: {len(graph.nodes)}")
    print(f"  Edges: {len(graph.edges)}")
    print(f"  Avg degree: {sum(n.degree for n in graph.nodes.values()) / len(graph.nodes):.1f}")
    
    # Time the algorithm
    import time
    
    assigner = FrequencyAssigner(graph)
    
    print(f"\nRunning DSATUR on large network...")
    start = time.time()
    stats = assigner.dsatur()
    elapsed = time.time() - start
    
    print(f"\nResults:")
    print(f"  Frequencies: {stats['chromatic_number']}")
    print(f"  Conflicts: {stats['conflicts']}")
    print(f"  Computation time: {elapsed:.2f} seconds")
    print(f"  Efficiency: {stats['efficiency']:.2f}%")
    print(f"  Nodes per second: {len(graph.nodes) / elapsed:.0f}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("GRAPH COLORING EXAMPLES")
    print("Network Frequency Assignment Use Cases")
    print("="*60)
    
    examples = [
        ("Simple Network", example_1_simple_network),
        ("Cellular Network", example_2_cellular_network),
        ("IoT Sensor Network", example_3_iot_network),
        ("WiFi Channels", example_4_wifi_channels),
        ("Custom Constraints", example_5_custom_constraints),
        ("Large Scale", example_6_large_scale),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n⚠ Error in {name}: {str(e)}")
    
    print("\n" + "="*60)
    print("✓ All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()