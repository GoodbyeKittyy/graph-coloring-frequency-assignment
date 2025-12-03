import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Download, Settings, Info } from 'lucide-react';

const FrequencyAssignmentViz = () => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [algorithm, setAlgorithm] = useState('dsatur');
  const [isRunning, setIsRunning] = useState(false);
  const [step, setStep] = useState(0);
  const [stats, setStats] = useState({ colors: 0, conflicts: 0, efficiency: 0 });
  const [speed, setSpeed] = useState(500);
  const [networkSize, setNetworkSize] = useState(30);
  const [showSettings, setShowSettings] = useState(false);

  const colors = [
    '#EF4444', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6',
    '#EC4899', '#14B8A6', '#F97316', '#6366F1', '#84CC16',
    '#06B6D4', '#F43F5E', '#8B5CF6', '#A3E635', '#22D3EE'
  ];

  const generateNetwork = (size) => {
    const newNodes = [];
    const newEdges = [];
    const width = 800;
    const height = 600;
    
    // Generate nodes in a grid-like pattern with randomness
    for (let i = 0; i < size; i++) {
      const angle = (i / size) * 2 * Math.PI;
      const radius = 150 + Math.random() * 150;
      newNodes.push({
        id: i,
        x: width / 2 + radius * Math.cos(angle) + (Math.random() - 0.5) * 50,
        y: height / 2 + radius * Math.sin(angle) + (Math.random() - 0.5) * 50,
        color: null,
        degree: 0,
        saturation: 0
      });
    }

    // Generate edges based on distance (interference range)
    const interferenceRange = 180;
    for (let i = 0; i < size; i++) {
      for (let j = i + 1; j < size; j++) {
        const dx = newNodes[i].x - newNodes[j].x;
        const dy = newNodes[i].y - newNodes[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < interferenceRange || Math.random() < 0.15) {
          newEdges.push({ from: i, to: j });
          newNodes[i].degree++;
          newNodes[j].degree++;
        }
      }
    }

    setNodes(newNodes);
    setEdges(newEdges);
    setStep(0);
    setStats({ colors: 0, conflicts: 0, efficiency: 0 });
  };

  useEffect(() => {
    generateNetwork(networkSize);
  }, [networkSize]);

  const getNeighborColors = (nodeId) => {
    const neighborColors = new Set();
    edges.forEach(edge => {
      if (edge.from === nodeId && nodes[edge.to].color !== null) {
        neighborColors.add(nodes[edge.to].color);
      }
      if (edge.to === nodeId && nodes[edge.from].color !== null) {
        neighborColors.add(nodes[edge.from].color);
      }
    });
    return neighborColors;
  };

  const getSmallestAvailableColor = (neighborColors) => {
    let color = 0;
    while (neighborColors.has(color)) {
      color++;
    }
    return color;
  };

  const welshPowell = () => {
    const sortedNodes = [...nodes].sort((a, b) => b.degree - a.degree);
    const newNodes = [...nodes];
    
    sortedNodes.forEach(node => {
      const neighborColors = getNeighborColors(node.id);
      newNodes[node.id].color = getSmallestAvailableColor(neighborColors);
    });
    
    return newNodes;
  };

  const dsatur = () => {
    const newNodes = nodes.map(n => ({ ...n, saturation: 0 }));
    let uncolored = new Set(nodes.map(n => n.id));
    
    // Color first node with highest degree
    const firstNode = [...newNodes].sort((a, b) => b.degree - a.degree)[0];
    newNodes[firstNode.id].color = 0;
    uncolored.delete(firstNode.id);
    
    // Update saturation for neighbors
    edges.forEach(edge => {
      if (edge.from === firstNode.id) newNodes[edge.to].saturation++;
      if (edge.to === firstNode.id) newNodes[edge.from].saturation++;
    });
    
    while (uncolored.size > 0) {
      // Find node with highest saturation (tie-break by degree)
      let maxNode = null;
      let maxSat = -1;
      let maxDeg = -1;
      
      uncolored.forEach(id => {
        const node = newNodes[id];
        if (node.saturation > maxSat || 
            (node.saturation === maxSat && node.degree > maxDeg)) {
          maxNode = node;
          maxSat = node.saturation;
          maxDeg = node.degree;
        }
      });
      
      // Color the selected node
      const neighborColors = getNeighborColors(maxNode.id);
      newNodes[maxNode.id].color = getSmallestAvailableColor(neighborColors);
      uncolored.delete(maxNode.id);
      
      // Update saturation for neighbors
      edges.forEach(edge => {
        if (edge.from === maxNode.id && uncolored.has(edge.to)) {
          const neighbor = newNodes[edge.to];
          const oldColors = getNeighborColors(edge.to);
          if (!oldColors.has(newNodes[maxNode.id].color)) {
            newNodes[edge.to].saturation++;
          }
        }
        if (edge.to === maxNode.id && uncolored.has(edge.from)) {
          const neighbor = newNodes[edge.from];
          const oldColors = getNeighborColors(edge.from);
          if (!oldColors.has(newNodes[maxNode.id].color)) {
            newNodes[edge.from].saturation++;
          }
        }
      });
    }
    
    return newNodes;
  };

  const runAlgorithm = () => {
    const coloredNodes = algorithm === 'dsatur' ? dsatur() : welshPowell();
    setNodes(coloredNodes);
    
    const usedColors = new Set(coloredNodes.map(n => n.color));
    const chromaticNumber = usedColors.size;
    
    // Calculate conflicts
    let conflicts = 0;
    edges.forEach(edge => {
      if (coloredNodes[edge.from].color === coloredNodes[edge.to].color) {
        conflicts++;
      }
    });
    
    // Calculate efficiency (inverse of chromatic number)
    const maxPossible = nodes.length;
    const efficiency = ((maxPossible - chromaticNumber) / maxPossible * 100).toFixed(1);
    
    setStats({
      colors: chromaticNumber,
      conflicts,
      efficiency
    });
  };

  const reset = () => {
    generateNetwork(networkSize);
    setIsRunning(false);
  };

  const exportData = () => {
    const data = {
      algorithm,
      nodes: nodes.length,
      edges: edges.length,
      chromaticNumber: stats.colors,
      conflicts: stats.conflicts,
      efficiency: stats.efficiency,
      assignments: nodes.map(n => ({ id: n.id, frequency: n.color }))
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'frequency-assignment.json';
    a.click();
  };

  return (
    <div className="w-full h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-6">
      <div className="max-w-7xl mx-auto h-full flex flex-col">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Network Frequency Assignment System</h1>
          <p className="text-slate-300">Advanced graph coloring for optimal spectrum allocation</p>
        </div>

        <div className="flex-1 flex gap-6">
          {/* Visualization Panel */}
          <div className="flex-1 bg-slate-800/50 rounded-lg border border-slate-700 p-4 relative">
            <svg width="100%" height="100%" viewBox="0 0 800 600">
              {/* Edges */}
              {edges.map((edge, i) => (
                <line
                  key={i}
                  x1={nodes[edge.from]?.x}
                  y1={nodes[edge.from]?.y}
                  x2={nodes[edge.to]?.x}
                  y2={nodes[edge.to]?.y}
                  stroke={
                    nodes[edge.from]?.color !== null && 
                    nodes[edge.from]?.color === nodes[edge.to]?.color
                      ? '#EF4444'
                      : '#475569'
                  }
                  strokeWidth={
                    nodes[edge.from]?.color !== null && 
                    nodes[edge.from]?.color === nodes[edge.to]?.color
                      ? 3
                      : 1
                  }
                  opacity={0.3}
                />
              ))}
              
              {/* Nodes */}
              {nodes.map((node, i) => (
                <g key={i}>
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={15}
                    fill={node.color !== null ? colors[node.color % colors.length] : '#64748b'}
                    stroke="#1e293b"
                    strokeWidth={2}
                  />
                  <text
                    x={node.x}
                    y={node.y}
                    textAnchor="middle"
                    dy="0.3em"
                    fontSize="10"
                    fill="white"
                    fontWeight="bold"
                  >
                    {node.color !== null ? `F${node.color}` : '?'}
                  </text>
                </g>
              ))}
            </svg>
            
            {/* Legend */}
            <div className="absolute bottom-6 left-6 bg-slate-900/80 p-3 rounded-lg border border-slate-700">
              <div className="text-xs space-y-1">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-slate-500"></div>
                  <span>Unassigned Node</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 bg-slate-600"></div>
                  <span>Interference Range</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 bg-red-500"></div>
                  <span className="text-red-400">Conflict (same frequency)</span>
                </div>
              </div>
            </div>
          </div>

          {/* Control Panel */}
          <div className="w-80 space-y-4">
            {/* Stats */}
            <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Info size={18} />
                Performance Metrics
              </h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-slate-400">Frequencies Used</div>
                  <div className="text-2xl font-bold text-blue-400">{stats.colors}</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Conflicts</div>
                  <div className={`text-2xl font-bold ${stats.conflicts === 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {stats.conflicts}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Spectrum Efficiency</div>
                  <div className="text-2xl font-bold text-purple-400">{stats.efficiency}%</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Network Size</div>
                  <div className="text-lg font-semibold">{nodes.length} nodes, {edges.length} links</div>
                </div>
              </div>
            </div>

            {/* Algorithm Selection */}
            <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
              <h3 className="font-semibold mb-3">Algorithm</h3>
              <select
                value={algorithm}
                onChange={(e) => setAlgorithm(e.target.value)}
                className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm"
              >
                <option value="dsatur">DSATUR (Degree of Saturation)</option>
                <option value="welsh-powell">Welsh-Powell</option>
              </select>
              <p className="text-xs text-slate-400 mt-2">
                {algorithm === 'dsatur' 
                  ? 'Prioritizes nodes with most colored neighbors - typically 45% better results'
                  : 'Colors nodes in decreasing order of degree - faster but less optimal'}
              </p>
            </div>

            {/* Settings */}
            <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="w-full flex items-center justify-between font-semibold mb-3"
              >
                <span className="flex items-center gap-2">
                  <Settings size={18} />
                  Network Settings
                </span>
                <span className="text-slate-400">{showSettings ? '▼' : '▶'}</span>
              </button>
              
              {showSettings && (
                <div className="space-y-3">
                  <div>
                    <label className="text-sm text-slate-400">Network Size: {networkSize} nodes</label>
                    <input
                      type="range"
                      min="10"
                      max="100"
                      value={networkSize}
                      onChange={(e) => setNetworkSize(Number(e.target.value))}
                      className="w-full mt-1"
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={runAlgorithm}
                  className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-medium flex items-center justify-center gap-2"
                >
                  <Play size={18} />
                  Run
                </button>
                <button
                  onClick={reset}
                  className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded font-medium flex items-center justify-center gap-2"
                >
                  <RotateCcw size={18} />
                  Reset
                </button>
                <button
                  onClick={exportData}
                  className="col-span-2 bg-green-600 hover:bg-green-700 px-4 py-2 rounded font-medium flex items-center justify-center gap-2"
                >
                  <Download size={18} />
                  Export Results
                </button>
              </div>
            </div>

            {/* Info */}
            <div className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-3 text-xs">
              <p className="text-blue-300">
                <strong>Use Case:</strong> This system assigns radio frequencies to cellular towers and IoT nodes to minimize interference while maximizing spectrum efficiency.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FrequencyAssignmentViz;