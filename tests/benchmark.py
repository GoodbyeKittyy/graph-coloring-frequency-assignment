"""
Performance benchmark script for graph coloring algorithms
"""

import time
import argparse
import sys
sys.path.insert(0, '..')

from graph_coloring import Graph, FrequencyAssigner, NetworkGenerator
import matplotlib.pyplot as plt


def benchmark_algorithm(algo_name, algo_func, graph, runs=5):
    """Benchmark a single algorithm"""
    times = []
    chromatic_numbers = []
    
    for _ in range(runs):
        start = time.time()
        stats = algo_func()
        elapsed = time.time() - start
        
        times.append(elapsed * 1000)  # Convert to ms
        chromatic_numbers.append(stats['chromatic_number'])
    
    return {
        'algorithm': algo_name,
        'avg_time_ms': sum(times) / len(times),
        'min_time_ms': min(times),
        'max_time_ms': max(times),
        'avg_colors': sum(chromatic_numbers) / len(chromatic_numbers),
        'best_colors': min(chromatic_numbers)
    }


def benchmark_scaling(max_nodes=1000, step=100):
    """Benchmark algorithms with increasing network sizes"""
    sizes = list(range(50, max_nodes + 1, step))
    results = {
        'sizes': sizes,
        'greedy': [],
        'welsh_powell': [],
        'dsatur': []
    }
    
    print(f"\nScaling Benchmark (up to {max_nodes} nodes)")
    print("=" * 60)
    
    for size in sizes:
        print(f"\nTesting with {size} nodes...")
        graph = NetworkGenerator.random_geometric(size, 250)
        assigner = FrequencyAssigner(graph)
        
        # Greedy
        start = time.time()
        assigner.greedy_coloring()
        results['greedy'].append((time.time() - start) * 1000)
        
        # Welsh-Powell
        start = time.time()
        assigner.welsh_powell()
        results['welsh_powell'].append((time.time() - start) * 1000)
        
        # DSATUR
        start = time.time()
        assigner.dsatur()
        results['dsatur'].append((time.time() - start) * 1000)
        
        print(f"  Greedy: {results['greedy'][-1]:.2f} ms")
        print(f"  Welsh-Powell: {results['welsh_powell'][-1]:.2f} ms")
        print(f"  DSATUR: {results['dsatur'][-1]:.2f} ms")
    
    return results


def plot_scaling_results(results):
    """Plot scaling benchmark results"""
    plt.figure(figsize=(10, 6))
    
    plt.plot(results['sizes'], results['greedy'], 
             marker='o', label='Greedy', linewidth=2)
    plt.plot(results['sizes'], results['welsh_powell'], 
             marker='s', label='Welsh-Powell', linewidth=2)
    plt.plot(results['sizes'], results['dsatur'], 
             marker='^', label='DSATUR', linewidth=2)
    
    plt.xlabel('Number of Nodes', fontsize=12)
    plt.ylabel('Time (ms)', fontsize=12)
    plt.title('Algorithm Scaling Performance', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('benchmark_scaling.png', dpi=300)
    print("\n✓ Saved scaling plot to benchmark_scaling.png")


def benchmark_quality(network_types, size=100):
    """Compare algorithm quality on different network types"""
    print(f"\nQuality Benchmark (network size: {size})")
    print("=" * 80)
    
    results = []
    
    for net_type, generator in network_types.items():
        print(f"\nNetwork Type: {net_type}")
        print("-" * 40)
        
        graph = generator(size)
        assigner = FrequencyAssigner(graph)
        
        for algo_name, algo_func in [
            ('Greedy', assigner.greedy_coloring),
            ('Welsh-Powell', assigner.welsh_powell),
            ('DSATUR', assigner.dsatur)
        ]:
            result = benchmark_algorithm(algo_name, algo_func, graph, runs=3)
            result['network_type'] = net_type
            results.append(result)
            
            print(f"  {algo_name:15} | "
                  f"Colors: {result['avg_colors']:4.1f} | "
                  f"Time: {result['avg_time_ms']:7.2f} ms")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Benchmark graph coloring algorithms'
    )
    parser.add_argument('--nodes', type=int, default=100,
                       help='Number of nodes for testing')
    parser.add_argument('--scaling', action='store_true',
                       help='Run scaling benchmark')
    parser.add_argument('--quality', action='store_true',
                       help='Run quality comparison')
    parser.add_argument('--all', action='store_true',
                       help='Run all benchmarks')
    parser.add_argument('--plot', action='store_true',
                       help='Generate plots')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("GRAPH COLORING ALGORITHM BENCHMARK")
    print("=" * 80)
    
    if args.all or args.quality:
        network_types = {
            'Random Geometric': lambda n: NetworkGenerator.random_geometric(n, 250),
            'Cellular Grid': lambda n: NetworkGenerator.cellular_grid(10, 10),
            'Scale-Free': lambda n: NetworkGenerator.scale_free(n, m=3)
        }
        benchmark_quality(network_types, args.nodes)
    
    if args.all or args.scaling:
        results = benchmark_scaling(max_nodes=500, step=50)
        
        if args.plot:
            try:
                plot_scaling_results(results)
            except ImportError:
                print("\n⚠ Matplotlib not installed. Skipping plot generation.")
    
    if not (args.scaling or args.quality or args.all):
        # Default: quick benchmark
        print(f"\nQuick Benchmark ({args.nodes} nodes, Random Geometric)")
        print("=" * 60)
        
        graph = NetworkGenerator.random_geometric(args.nodes, 250)
        assigner = FrequencyAssigner(graph)
        
        print(f"\nNetwork: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        print("-" * 60)
        
        for algo_name, algo_func in [
            ('Greedy', assigner.greedy_coloring),
            ('Welsh-Powell', assigner.welsh_powell),
            ('DSATUR', assigner.dsatur)
        ]:
            result = benchmark_algorithm(algo_name, algo_func, graph)
            print(f"\n{algo_name}:")
            print(f"  Chromatic Number: {result['best_colors']}")
            print(f"  Average Time: {result['avg_time_ms']:.2f} ms")
            print(f"  Min Time: {result['min_time_ms']:.2f} ms")
            print(f"  Max Time: {result['max_time_ms']:.2f} ms")
    
    print("\n" + "=" * 80)
    print("✓ Benchmark complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()