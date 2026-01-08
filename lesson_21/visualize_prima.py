import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from heapq import heappush, heappop
from copy import deepcopy


def prim_mst_visual(graph):
    mst = nx.Graph()
    visited = {list(graph.nodes())[1]}
    edges = []
    for _, v, weight in graph.edges(data="weight", nbunch=visited):
        heappush(edges, (weight, _, v))

    states = []
    states.append(
        {
            "step": 0,
            "visited": visited.copy(),
            "mst_edges": [],
            "current_edge": None,
            "description": "Початковий стан: вибрана вершина " + list(visited)[0],
            "edges_queue": deepcopy(edges),
        }
    )

    step = 1
    while visited != set(graph.nodes()):
        weight, u, v = heappop(edges)
        if v not in visited:
            states.append(
                {
                    "step": step,
                    "visited": visited.copy(),
                    "mst_edges": [(a, b, c) for a, b, c in mst.edges(data="weight")],
                    "current_edge": (u, v, weight),
                    "description": f"Розглядаємо ребро {u}-{v} з вагою {weight}",
                    "edges_queue": deepcopy(edges),
                }
            )
            step += 1

            visited.add(v)
            mst.add_edge(u, v, weight=weight)

            states.append(
                {
                    "step": step,
                    "visited": visited.copy(),
                    "mst_edges": [(a, b, c) for a, b, c in mst.edges(data="weight")],
                    "current_edge": None,
                    "description": f"Додано вершину {v} та ребро {u}-{v} до MST",
                    "edges_queue": deepcopy(edges),
                }
            )
            step += 1

            for _, new_v, new_weight in graph.edges(data="weight", nbunch=[v]):
                if new_v not in visited:
                    heappush(edges, (new_weight, v, new_v))

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
    states = prim_mst_visual(G)

    st.title("Візуалізація алгоритму Прима")

    if "step" not in st.session_state:
        st.session_state.step = 0

    current_state = states[st.session_state.step]

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, ax=ax, node_color="lightgray", edge_color="gray")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=nx.get_edge_attributes(G, "weight"), ax=ax
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=list(current_state["visited"]), node_color="green", ax=ax
    )

    mst_edges = [(u, v) for u, v, _ in current_state["mst_edges"]]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color="red", width=2, ax=ax)

    if current_state["current_edge"]:
        u, v, _ = current_state["current_edge"]
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)], edge_color="blue", width=3, ax=ax
        )

    st.pyplot(fig)
    st.write(current_state["description"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Попередній крок"):
            if st.session_state.step > 0:
                st.session_state.step -= 1
                st.rerun()
    with col2:
        if st.button("Наступний крок"):
            if st.session_state.step < len(states) - 1:
                st.session_state.step += 1
                st.rerun()

    st.write(f"Крок {current_state['step']} з {len(states) - 1}")
