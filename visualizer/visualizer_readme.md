# 🎨 Network Frequency Assignment Visualizer

Interactive web-based visualization for graph coloring algorithms.

## 🚀 Quick Start

### Option 1: Open Directly (Easiest)
Simply double-click `index.html` to open in your web browser. No server needed!

### Option 2: Local Server (Recommended for Development)

```bash
# Using Python
cd visualizer
python -m http.server 8000

# Then open: http://localhost:8000
```

Or using Node.js:
```bash
npm install -g http-server
cd visualizer
http-server
```

## ✨ Features

- **Real-time Visualization**: Watch algorithms color the network step-by-step
- **Multiple Algorithms**: 
  - DSATUR (Degree of Saturation) - Best quality
  - Welsh-Powell - Faster alternative
- **Interactive Controls**:
  - Adjust network size (10-100 nodes)
  - Generate random topologies
  - Export results to JSON
- **Performance Metrics**:
  - Frequencies used (chromatic number)
  - Conflict detection
  - Spectrum efficiency percentage
- **Visual Feedback**:
  - Color-coded nodes by frequency
  - Red links indicate conflicts
  - Real-time statistics

## 🎮 How to Use

1. **Open** `index.html` in your browser
2. **Adjust** network size using the slider (default: 30 nodes)
3. **Select** algorithm (DSATUR recommended)
4. **Click** "Run" to assign frequencies
5. **View** results in the metrics panel
6. **Export** data using "Export Results" button

## 🎨 Understanding the Visualization

### Node Colors
- **Gray**: Unassigned frequency
- **Colors**: Each color represents a different frequency (F0, F1, F2, etc.)

### Edge Colors
- **Gray**: Normal interference link
- **Red**: Conflict (both nodes using same frequency - should be 0 with good algorithms)

### Metrics
- **Frequencies Used**: Total number of frequencies needed (lower is better)
- **Conflicts**: Number of adjacent nodes with same frequency (should be 0)
- **Spectrum Efficiency**: How well we minimized frequency usage (higher is better)

## 🔧 Customization

The visualizer is self-contained in `index.html`. To customize:

1. **Colors**: Modify the `colors` array around line 40
2. **Network Generation**: Adjust `generateNetwork()` function
3. **Styling**: Change Tailwind classes in JSX
4. **Algorithms**: Add new algorithms by creating functions like `dsatur()` and `welshPowell()`

## 📊 Export Format

Exported JSON structure:
```json
{
  "algorithm": "DSATUR",
  "nodes": 30,
  "edges": 85,
  "chromaticNumber": 8,
  "conflicts": 0,
  "efficiency": 73.3,
  "assignments": [
    {"id": 0, "frequency": 0},
    {"id": 1, "frequency": 1},
    ...
  ]
}
```

## 🐛 Troubleshooting

### Visualizer won't load
- Check browser console (F12) for errors
- Ensure you have internet connection (CDN resources)
- Try a different browser (Chrome, Firefox, Safari)

### Slow performance with large networks
- Reduce network size below 50 nodes
- Close other browser tabs
- Try Welsh-Powell algorithm (faster)

### Export not working
- Check browser download settings
- Allow pop-ups for this page
- Check Downloads folder

## 🌐 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 💡 Tips

1. **Start small**: Begin with 10-20 nodes to understand the algorithms
2. **Compare algorithms**: Run both DSATUR and Welsh-Powell on same network
3. **Look for patterns**: Notice how high-degree nodes get colored first
4. **Check conflicts**: Red links indicate algorithm errors (rare with DSATUR)
5. **Export data**: Use JSON output with Python backend for analysis

## 🔗 Integration with Python

Use exported data with the Python implementation:

```python
import json
from graph_coloring import Graph, FrequencyAssigner

# Load visualizer export
with open('frequency-assignment.json') as f:
    data = json.load(f)

# Verify results
print(f"Chromatic number: {data['chromaticNumber']}")
print(f"Efficiency: {data['efficiency']}%")
```

## 📚 Learn More

- Main README: `../README.md`
- Python Implementation: `../graph_coloring.py`
- C++ Version: `../graph_coloring.cpp`
- Examples: `../examples/basic_usage.py`

## 🎓 Educational Use

Perfect for:
- Understanding graph coloring algorithms
- Teaching network optimization
- Demonstrating frequency assignment
- Conference presentations
- Project demonstrations

## 🤝 Contributing

To add new features:
1. Edit `index.html`
2. Test in browser
3. Document changes here
4. Submit pull request

---

**Questions?** Open an issue on GitHub or check the main README.