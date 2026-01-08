import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from copy import deepcopy

def kruskal_mst_visual(graph):
    forest = nx.Graph()
    for node in graph.nodes():
        forest.add_node(node)
    
    sorted_edges = sorted(graph.edges(data=True), key=lambda t: t[2].get("weight", 1))
    mst = nx.Graph()
    
    states = []
    states.append({
        'step': 0,
        'forest': forest.copy(),
        'mst_edges': [],
        'current_edge': None,
        'description': 'Початковий стан: кожна вершина є окремим деревом',
        'sorted_edges': deepcopy(sorted_edges)
    })
    
    step = 1
    for edge in sorted_edges:
        u, v, weight = edge
        if not nx.has_path(forest, u, v):
            states.append({
                'step': step,
                'forest': forest.copy(),
                'mst_edges': [(a,b,c) for a,b,c in mst.edges(data='weight')],
                'current_edge': (u, v, weight['weight']),
                'description': f'Розглядаємо ребро {u}-{v} з вагою {weight["weight"]}',
                'sorted_edges': deepcopy(sorted_edges)
            })
            step += 1
            
            forest.add_edge(u, v)
            mst.add_edge(u, v, weight=weight['weight'])
            
            states.append({
                'step': step,
                'forest': forest.copy(),
                'mst_edges': [(a,b,c) for a,b,c in mst.edges(data='weight')],
                'current_edge': None,
                'description': f'Додано ребро {u}-{v} до MST (не утворює цикл)',
                'sorted_edges': deepcopy(sorted_edges)
            })
            step += 1
    
    return states

if __name__ == "__main__":
    G = nx.Graph()
    G.add_edge("A", "B", weight=7)
    G.add_edge("A", "D", weight=5)
    G.add_edge("B", "C", weight=8)
    G.add_edge("B", "D", weight=9)
    G.add_edge("B", "E", weight=7)
    G.add_edge("C", "E", weight=5)
    G.add_edge("D", "E", weight=15)
    G.add_edge("D", "F", weight=6)
    G.add_edge("E", "F", weight=8)
    G.add_edge("E", "G", weight=9)
    G.add_edge("F", "G", weight=11)
    
    pos = nx.spring_layout(G, seed=42)
    states = kruskal_mst_visual(G)
    
    st.title("Візуалізація алгоритму Краскала")
    
    if 'step' not in st.session_state:
        st.session_state.step = 0
    
    current_state = states[st.session_state.step]
    
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightgray', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
    
    mst_edges = [(u,v) for u,v,_ in current_state['mst_edges']]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=2, ax=ax)
    
    if current_state['current_edge']:
        u,v,_ = current_state['current_edge']
        nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color='blue', width=3, ax=ax)
    
    st.pyplot(fig)
    st.write(current_state['description'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Попередній крок'):
            if st.session_state.step > 0:
                st.session_state.step -= 1
                st.rerun()
    with col2:
        if st.button('Наступний крок'):
            if st.session_state.step < len(states)-1:
                st.session_state.step += 1
                st.rerun()
    
    st.write(f"Крок {current_state['step']} з {len(states)-1}")