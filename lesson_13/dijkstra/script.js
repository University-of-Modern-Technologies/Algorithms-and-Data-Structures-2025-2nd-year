/**
 * Dijkstra's Algorithm Visualization
 * Encapsulated in an IIFE (Immediately Invoked Function Expression)
 * to avoid polluting the global namespace.
 */
(() => {
    // ==========================================
    // Constants & Configuration
    // ==========================================
    const NODES = [
        { id: 'A', x: 100, y: 300 },
        { id: 'B', x: 300, y: 100 },
        { id: 'C', x: 300, y: 500 },
        { id: 'D', x: 500, y: 100 },
        { id: 'E', x: 500, y: 500 },
        { id: 'F', x: 700, y: 300 }
    ];

    const EDGES = [
        { from: 'A', to: 'B', weight: 4 },
        { from: 'A', to: 'C', weight: 2 },
        { from: 'C', to: 'B', weight: 1 }, // A->C->B (2+1=3)
        { from: 'B', to: 'D', weight: 5 },
        { from: 'C', to: 'E', weight: 10 },
        { from: 'C', to: 'D', weight: 8 },
        { from: 'D', to: 'E', weight: 2 },
        { from: 'D', to: 'F', weight: 6 },
        { from: 'E', to: 'F', weight: 3 }
    ];

    // ==========================================
    // State Management
    // ==========================================
    const state = {
        distances: {},
        previous: {},
        visited: new Set(),
        unvisited: new Set(),
        bestEdges: {}, // Map nodeID -> edgeID
        generator: null,
        isAutoPlaying: false,
        autoPlayInterval: null
    };

    // ==========================================
    // DOM Elements
    // ==========================================
    const ui = {
        svg: document.getElementById('graph-svg'),
        tableBody: document.querySelector('#distance-table tbody'),
        logContainer: document.getElementById('log-container'),
        btnStart: document.getElementById('btn-start'),
        btnNext: document.getElementById('btn-next'),
        btnReset: document.getElementById('btn-reset')
    };

    // ==========================================
    // Initialization
    // ==========================================
    function init() {
        drawGraph();
        resetAlgorithm();
        bindEvents();
    }

    function bindEvents() {
        ui.btnStart.addEventListener('click', toggleAutoPlay);
        ui.btnNext.addEventListener('click', nextStep);
        ui.btnReset.addEventListener('click', () => {
            stopAutoPlay();
            resetAlgorithm();
        });
    }

    function resetAlgorithm() {
        state.distances = {};
        state.previous = {};
        state.visited.clear();
        state.unvisited.clear();
        state.bestEdges = {};
        
        NODES.forEach(node => {
            state.distances[node.id] = Infinity;
            state.previous[node.id] = null;
            state.unvisited.add(node.id);
        });
        
        // Start at A
        state.distances['A'] = 0;
        
        state.generator = dijkstraGenerator();
        
        updateTable();
        log("Algorithm reset. Ready to start from Node A.", false);
        resetVisuals();
    }

    function resetVisuals() {
        document.querySelectorAll('.graph__node-circle').forEach(el => {
            el.classList.remove('graph__node-circle--visited', 'graph__node-circle--current');
        });
        document.querySelectorAll('.graph__edge').forEach(el => {
            el.classList.remove('graph__edge--active', 'graph__edge--path');
            el.setAttribute('marker-end', 'url(#arrowhead)');
        });
        
        NODES.forEach(node => {
            const textEl = document.getElementById(`dist-${node.id}`);
            if(textEl) textEl.textContent = '∞';
        });
        document.getElementById(`dist-A`).textContent = '0';
    }

    // ==========================================
    // Visualization / Drawing
    // ==========================================
    function drawGraph() {
        ui.svg.innerHTML = `
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#475569"/>
                </marker>
                <marker id="arrowhead-active" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#38bdf8"/>
                </marker>
                <marker id="arrowhead-path" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#a855f7"/>
                </marker>
            </defs>
        `;

        // Draw Edges
        EDGES.forEach(edge => {
            const fromNode = NODES.find(n => n.id === edge.from);
            const toNode = NODES.find(n => n.id === edge.to);
            
            const line = createSvgElement('line', {
                x1: fromNode.x, y1: fromNode.y,
                x2: toNode.x, y2: toNode.y,
                class: 'graph__edge',
                id: `edge-${edge.from}-${edge.to}`,
                'marker-end': 'url(#arrowhead)'
            });
            ui.svg.appendChild(line);

            // Weight Label
            const midX = (fromNode.x + toNode.x) / 2;
            const midY = (fromNode.y + toNode.y) / 2;
            const text = createSvgElement('text', {
                x: midX, y: midY - 10,
                class: 'graph__edge-weight'
            });
            text.textContent = edge.weight;
            ui.svg.appendChild(text);
        });

        // Draw Nodes
        NODES.forEach(node => {
            const g = createSvgElement('g');
            
            const circle = createSvgElement('circle', {
                cx: node.x, cy: node.y, r: 20,
                class: 'graph__node-circle',
                id: `node-${node.id}`
            });
            
            const label = createSvgElement('text', {
                x: node.x, y: node.y,
                class: 'graph__node-text'
            });
            label.textContent = node.id;

            const distLabel = createSvgElement('text', {
                x: node.x, y: node.y - 30,
                class: 'graph__node-dist',
                id: `dist-${node.id}`,
                style: 'font-weight: bold; font-size: 14px; fill: #38bdf8;'
            });
            distLabel.textContent = node.id === 'A' ? '0' : '∞';

            g.appendChild(circle);
            g.appendChild(label);
            g.appendChild(distLabel);
            ui.svg.appendChild(g);
        });
    }

    function createSvgElement(type, attributes = {}) {
        const el = document.createElementNS("http://www.w3.org/2000/svg", type);
        for (const [key, value] of Object.entries(attributes)) {
            el.setAttribute(key, value);
        }
        return el;
    }

    // ==========================================
    // Algorithm Logic (Generator)
    // ==========================================
    function* dijkstraGenerator() {
        while (state.unvisited.size > 0) {
            // 1. Select node with smallest distance
            let currentNode = null;
            let minDist = Infinity;

            state.unvisited.forEach(nodeId => {
                if (state.distances[nodeId] < minDist) {
                    minDist = state.distances[nodeId];
                    currentNode = nodeId;
                }
            });

            if (currentNode === null || state.distances[currentNode] === Infinity) {
                log("No more reachable nodes. Algorithm finished.");
                break;
            }

            highlightNode(currentNode, 'current');
            log(`Visiting Node ${currentNode} (Distance: ${state.distances[currentNode]})`, true);
            yield;

            // 2. Check neighbors
            const neighbors = EDGES.filter(e => e.from === currentNode);
            
            for (const edge of neighbors) {
                if (!state.visited.has(edge.to)) {
                    const neighbor = edge.to;
                    const newDist = state.distances[currentNode] + edge.weight;
                    
                    highlightEdge(currentNode, neighbor, 'active');
                    log(`Checking neighbor ${neighbor} via edge weight ${edge.weight}...`);
                    yield;

                    if (newDist < state.distances[neighbor]) {
                        log(`Found shorter path to ${neighbor}! ${state.distances[neighbor] === Infinity ? '∞' : state.distances[neighbor]} -> ${newDist}`, true);
                        state.distances[neighbor] = newDist;
                        state.previous[neighbor] = currentNode;
                        updateNodeDistLabel(neighbor, newDist);
                        updatePathVisuals(neighbor, currentNode, edge.from, edge.to);
                        updateTable();
                        yield;
                    } else {
                        log(`Path to ${neighbor} (${newDist}) is not shorter than current (${state.distances[neighbor]}).`);
                    }
                    
                    highlightEdge(currentNode, neighbor, 'inactive');
                }
            }

            // 3. Mark as visited
            state.visited.add(currentNode);
            state.unvisited.delete(currentNode);
            highlightNode(currentNode, 'visited');
            log(`Finished processing Node ${currentNode}.`);
            updateTable();
            yield;
        }
        
        log("Dijkstra's Algorithm Complete!");
        stopAutoPlay();
    }

    // ==========================================
    // Control Logic
    // ==========================================
    function nextStep() {
        if (!state.generator) return;
        
        const result = state.generator.next();
        if (result.done) {
            ui.btnNext.disabled = true;
            ui.btnStart.disabled = true;
        }
    }

    function toggleAutoPlay() {
        if (state.isAutoPlaying) {
            stopAutoPlay();
        } else {
            startAutoPlay();
        }
    }

    function startAutoPlay() {
        state.isAutoPlaying = true;
        ui.btnStart.textContent = "Pause";
        ui.btnStart.classList.remove('button--primary');
        ui.btnStart.classList.add('button--secondary');
        
        nextStep();
        state.autoPlayInterval = setInterval(() => {
            if (state.generator && !ui.btnNext.disabled) {
                nextStep();
            } else {
                stopAutoPlay();
            }
        }, 1000);
    }

    function stopAutoPlay() {
        state.isAutoPlaying = false;
        clearInterval(state.autoPlayInterval);
        ui.btnStart.textContent = "Start / Auto";
        ui.btnStart.classList.add('button--primary');
        ui.btnStart.classList.remove('button--secondary');
    }

    // ==========================================
    // UI Helpers
    // ==========================================
    function log(message, highlight = false) {
        const div = document.createElement('div');
        div.className = `log__entry ${highlight ? 'log__entry--highlight' : ''}`;
        div.textContent = message;
        ui.logContainer.appendChild(div);
        ui.logContainer.scrollTop = ui.logContainer.scrollHeight;
    }

    function updateTable() {
        ui.tableBody.innerHTML = '';
        NODES.forEach(node => {
            const tr = document.createElement('tr');
            const dist = state.distances[node.id] === Infinity ? '∞' : state.distances[node.id];
            const prev = state.previous[node.id] || '-';
            
            tr.innerHTML = `
                <td>${node.id}</td>
                <td>${dist}</td>
                <td>${prev}</td>
            `;
            ui.tableBody.appendChild(tr);
        });
    }

    function highlightNode(nodeId, type) {
        if (type === 'current') {
            document.querySelectorAll('.graph__node-circle').forEach(el => el.classList.remove('graph__node-circle--current'));
        }
        
        const el = document.getElementById(`node-${nodeId}`);
        if (el) {
            if (type === 'visited') {
                el.classList.remove('graph__node-circle--current');
                el.classList.add('graph__node-circle--visited');
            } else {
                el.classList.add('graph__node-circle--current');
            }
        }
    }

    function highlightEdge(from, to, status) {
        const el = document.getElementById(`edge-${from}-${to}`);
        if (el) {
            if (status === 'active') {
                el.classList.add('graph__edge--active');
                el.setAttribute('marker-end', 'url(#arrowhead-active)');
            } else {
                el.classList.remove('graph__edge--active');
                if (el.classList.contains('graph__edge--path')) {
                    el.setAttribute('marker-end', 'url(#arrowhead-path)');
                } else {
                    el.setAttribute('marker-end', 'url(#arrowhead)');
                }
            }
        }
    }

    function updatePathVisuals(targetNode, fromNode, edgeFrom, edgeTo) {
        if (state.bestEdges[targetNode]) {
            const oldEdge = document.getElementById(state.bestEdges[targetNode]);
            if (oldEdge) {
                oldEdge.classList.remove('graph__edge--path');
                oldEdge.setAttribute('marker-end', 'url(#arrowhead)');
            }
        }

        const newEdgeId = `edge-${edgeFrom}-${edgeTo}`;
        state.bestEdges[targetNode] = newEdgeId;
        const newEdge = document.getElementById(newEdgeId);
        if (newEdge) {
            newEdge.classList.add('graph__edge--path');
            newEdge.setAttribute('marker-end', 'url(#arrowhead-path)');
        }
    }

    function updateNodeDistLabel(nodeId, dist) {
        const el = document.getElementById(`dist-${nodeId}`);
        if (el) el.textContent = dist;
    }

    // Start Application
    init();

})();
