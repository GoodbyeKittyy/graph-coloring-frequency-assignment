#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <queue>
#include <unordered_map>
#include <cmath>

using namespace std;

struct Node {
    int id;
    int color;
    int degree;
    int saturation;
    set<int> neighbors;
    pair<double, double> position;
    
    Node(int id_ = 0) : id(id_), color(-1), degree(0), saturation(0), position({0.0, 0.0}) {}
};

class Graph {
private:
    unordered_map<int, Node> nodes;
    vector<pair<int, int>> edges;
    
public:
    void addNode(int id, double x = 0.0, double y = 0.0) {
        if (nodes.find(id) == nodes.end()) {
            nodes[id] = Node(id);
            nodes[id].position = {x, y};
        }
    }
    
    void addEdge(int u, int v) {
        if (nodes.find(u) == nodes.end() || nodes.find(v) == nodes.end()) {
            cerr << "Error: Node not found" << endl;
            return;
        }
        
        if (u != v && nodes[u].neighbors.find(v) == nodes[u].neighbors.end()) {
            edges.push_back({u, v});
            nodes[u].neighbors.insert(v);
            nodes[v].neighbors.insert(u);
            nodes[u].degree++;
            nodes[v].degree++;
        }
    }
    
    set<int> getNeighborColors(int nodeId) {
        set<int> colors;
        for (int neighbor : nodes[nodeId].neighbors) {
            if (nodes[neighbor].color != -1) {
                colors.insert(nodes[neighbor].color);
            }
        }
        return colors;
    }
    
    int getSmallestAvailableColor(const set<int>& neighborColors) {
        int color = 0;
        while (neighborColors.find(color) != neighborColors.end()) {
            color++;
        }
        return color;
    }
    
    void resetColors() {
        for (auto& [id, node] : nodes) {
            node.color = -1;
            node.saturation = 0;
        }
    }
    
    int getChromaticNumber() {
        set<int> colors;
        for (const auto& [id, node] : nodes) {
            if (node.color != -1) {
                colors.insert(node.color);
            }
        }
        return colors.size();
    }
    
    int countConflicts() {
        int conflicts = 0;
        for (const auto& [u, v] : edges) {
            if (nodes[u].color != -1 && nodes[v].color != -1 && 
                nodes[u].color == nodes[v].color) {
                conflicts++;
            }
        }
        return conflicts;
    }
    
    // Welsh-Powell Algorithm
    pair<int, double> welshPowell() {
        auto start = chrono::high_resolution_clock::now();
        resetColors();
        
        // Sort nodes by degree (descending)
        vector<int> sortedNodes;
        for (const auto& [id, node] : nodes) {
            sortedNodes.push_back(id);
        }
        
        sort(sortedNodes.begin(), sortedNodes.end(), 
             [this](int a, int b) { return nodes[a].degree > nodes[b].degree; });
        
        // Color each node
        for (int nodeId : sortedNodes) {
            set<int> neighborColors = getNeighborColors(nodeId);
            nodes[nodeId].color = getSmallestAvailableColor(neighborColors);
        }
        
        auto end = chrono::high_resolution_clock::now();
        double elapsed = chrono::duration<double, milli>(end - start).count();
        
        return {getChromaticNumber(), elapsed};
    }
    
    // DSATUR Algorithm (Degree of Saturation)
    pair<int, double> dsatur() {
        auto start = chrono::high_resolution_clock::now();
        resetColors();
        
        set<int> uncolored;
        for (const auto& [id, node] : nodes) {
            uncolored.insert(id);
        }
        
        if (uncolored.empty()) {
            return {0, 0.0};
        }
        
        // Color node with highest degree first
        int firstNode = *max_element(uncolored.begin(), uncolored.end(),
            [this](int a, int b) { return nodes[a].degree < nodes[b].degree; });
        
        nodes[firstNode].color = 0;
        uncolored.erase(firstNode);
        
        // Update saturation for neighbors
        for (int neighbor : nodes[firstNode].neighbors) {
            if (uncolored.find(neighbor) != uncolored.end()) {
                nodes[neighbor].saturation++;
            }
        }
        
        // Color remaining nodes
        while (!uncolored.empty()) {
            // Find node with highest saturation (tie-break by degree)
            int selected = *max_element(uncolored.begin(), uncolored.end(),
                [this](int a, int b) {
                    if (nodes[a].saturation != nodes[b].saturation) {
                        return nodes[a].saturation < nodes[b].saturation;
                    }
                    return nodes[a].degree < nodes[b].degree;
                });
            
            // Color the selected node
            set<int> neighborColors = getNeighborColors(selected);
            nodes[selected].color = getSmallestAvailableColor(neighborColors);
            uncolored.erase(selected);
            
            // Update saturation for uncolored neighbors
            for (int neighbor : nodes[selected].neighbors) {
                if (uncolored.find(neighbor) != uncolored.end()) {
                    set<int> colors = getNeighborColors(neighbor);
                    nodes[neighbor].saturation = colors.size();
                }
            }
        }
        
        auto end = chrono::high_resolution_clock::now();
        double elapsed = chrono::duration<double, milli>(end - start).count();
        
        return {getChromaticNumber(), elapsed};
    }
    
    // Greedy Coloring
    pair<int, double> greedyColoring() {
        auto start = chrono::high_resolution_clock::now();
        resetColors();
        
        for (auto& [id, node] : nodes) {
            set<int> neighborColors = getNeighborColors(id);
            node.color = getSmallestAvailableColor(neighborColors);
        }
        
        auto end = chrono::high_resolution_clock::now();
        double elapsed = chrono::duration<double, milli>(end - start).count();
        
        return {getChromaticNumber(), elapsed};
    }
    
    void printStats(const string& algorithm, int chromatic, double time) {
        int conflicts = countConflicts();
        double efficiency = (nodes.size() - chromatic) / (double)nodes.size() * 100.0;
        
        cout << "\n" << algorithm << " Algorithm Results:" << endl;
        cout << "  Nodes: " << nodes.size() << endl;
        cout << "  Edges: " << edges.size() << endl;
        cout << "  Chromatic Number: " << chromatic << endl;
        cout << "  Conflicts: " << conflicts << endl;
        cout << "  Efficiency: " << efficiency << "%" << endl;
        cout << "  Time: " << time << " ms" << endl;
    }
    
    void exportToJSON(const string& filename, const string& algorithm) {
        ofstream file(filename);
        if (!file.is_open()) {
            cerr << "Error: Cannot open file " << filename << endl;
            return;
        }
        
        file << "{\n";
        file << "  \"algorithm\": \"" << algorithm << "\",\n";
        file << "  \"chromatic_number\": " << getChromaticNumber() << ",\n";
        file << "  \"conflicts\": " << countConflicts() << ",\n";
        file << "  \"nodes\": " << nodes.size() << ",\n";
        file << "  \"edges\": " << edges.size() << ",\n";
        file << "  \"assignments\": [\n";
        
        bool first = true;
        for (const auto& [id, node] : nodes) {
            if (!first) file << ",\n";
            file << "    {\"id\": " << id 
                 << ", \"frequency\": " << node.color 
                 << ", \"degree\": " << node.degree << "}";
            first = false;
        }
        
        file << "\n  ]\n";
        file << "}\n";
        file.close();
        
        cout << "✓ Exported to " << filename << endl;
    }
    
    size_t getNumNodes() const { return nodes.size(); }
    size_t getNumEdges() const { return edges.size(); }
};

class NetworkGenerator {
public:
    // Generate random geometric graph
    static Graph randomGeometric(int numNodes, double radius, double width = 1000, double height = 1000) {
        Graph graph;
        vector<pair<double, double>> positions;
        
        // Generate random positions
        srand(time(nullptr));
        for (int i = 0; i < numNodes; i++) {
            double x = (rand() / (double)RAND_MAX) * width;
            double y = (rand() / (double)RAND_MAX) * height;
            positions.push_back({x, y});
            graph.addNode(i, x, y);
        }
        
        // Add edges based on distance
        for (int i = 0; i < numNodes; i++) {
            for (int j = i + 1; j < numNodes; j++) {
                double dx = positions[i].first - positions[j].first;
                double dy = positions[i].second - positions[j].second;
                double dist = sqrt(dx * dx + dy * dy);
                
                if (dist <= radius) {
                    graph.addEdge(i, j);
                }
            }
        }
        
        return graph;
    }
    
    // Generate cellular grid
    static Graph cellularGrid(int rows, int cols) {
        Graph graph;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                int nodeId = i * cols + j;
                graph.addNode(nodeId, j * 100.0, i * 100.0);
            }
        }
        
        // Add edges
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                int nodeId = i * cols + j;
                
                if (j < cols - 1) {
                    graph.addEdge(nodeId, nodeId + 1);
                }
                
                if (i < rows - 1) {
                    graph.addEdge(nodeId, nodeId + cols);
                }
                
                // Hex pattern
                if (i < rows - 1 && j > 0) {
                    graph.addEdge(nodeId, nodeId + cols - 1);
                }
                if (i < rows - 1 && j < cols - 1) {
                    graph.addEdge(nodeId, nodeId + cols + 1);
                }
            }
        }
        
        return graph;
    }
};

int main() {
    cout << "========================================" << endl;
    cout << "NETWORK FREQUENCY ASSIGNMENT - C++" << endl;
    cout << "High-Performance Graph Coloring" << endl;
    cout << "========================================" << endl;
    
    // Generate network
    cout << "\nGenerating random geometric network..." << endl;
    Graph graph = NetworkGenerator::randomGeometric(100, 250);
    cout << "✓ Generated " << graph.getNumNodes() << " nodes, " 
         << graph.getNumEdges() << " interference links" << endl;
    
    // Test algorithms
    cout << "\n--- ALGORITHM COMPARISON ---" << endl;
    
    auto [greedy_colors, greedy_time] = graph.greedyColoring();
    graph.printStats("Greedy", greedy_colors, greedy_time);
    
    auto [wp_colors, wp_time] = graph.welshPowell();
    graph.printStats("Welsh-Powell", wp_colors, wp_time);
    
    auto [dsatur_colors, dsatur_time] = graph.dsatur();
    graph.printStats("DSATUR", dsatur_colors, dsatur_time);
    
    // Export best result
    cout << "\nExporting results..." << endl;
    graph.exportToJSON("frequency_assignment_cpp.json", "DSATUR");
    
    cout << "\n========================================" << endl;
    cout << "✓ Analysis complete!" << endl;
    cout << "========================================" << endl;
    
    return 0;
}