import graphviz
import streamlit as st
import networkx as nx


def output_node_and_edges(graph: nx.Graph):
    st.info(graph.nodes)
    st.info(graph.edges)


def count_nodes(graph: nx.Graph):
    num_nodes = len(graph.nodes)
    num_edges = len(graph.edges)
    st.info(f"No. of nodes is {num_nodes} and No. of Edges are {num_edges}")


def specific_node(graph, the_node):
    if graph.has_node(the_node):
        st.info(f"{the_node} found in the data")
    else:
        st.info(f"{the_node} not found in the data")


def specific_edge(graph, source, target):
    if source == target:
        st.error("Please select different people")
    elif graph.has_edge(source, target):
        st.info(f"Relation between {source} and {target} found in the data")
    else:
        st.info(f"Relation between {source} and {target} not found in the data")


def random_relation(graph, source, target):
    if source == target:
        st.error("Please select different people")
    else:
        try:
            nx.has_path(graph, source, target)
            st.info(f"Relation between {source} and {target} found in the data")
        except nx.NetworkXNoPath:
            st.info(f"Relation between {source} and {target} not found in the data")


def density(graph: nx.Graph):
    num_nodes = len(graph.nodes)
    num_edges = len(graph.edges)
    if num_edges == 0 or num_nodes <= 1:
        return 0
    density_graph = num_edges / (num_nodes * (num_nodes - 1))
    if not graph.is_directed():
        density_graph *= 2
    st.info(f"The density of the graph is {density_graph}")


def graph_directed(graph: nx.Graph):
    if graph.is_directed():
        st.info("The Graph is Directed")
    else:
        st.info("The Graph is not Directed")


def graph_emptiness(graph: nx.Graph):
    num_edges = len(graph.edges)
    if num_edges == 0:
        st.info("The graph is Empty")
    else:
        st.info("The graph is not empty")


def graph_dict_func():
    graph_dict = {
        "nodes": st.session_state["person_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict


def shortest_path(graph: nx.Graph):
    person_1_col, person_2_col = st.columns(2)
    with person_1_col:
        person_1_sel = st.selectbox(
            "Select Person 1",
            options=graph.nodes
        )
    with person_2_col:
        person_2_sel = st.selectbox(
            "Select Person 2",
            options=graph.nodes
        )
    find_path_button = st.button('Find the path', type="primary")

    if find_path_button:
        if person_1_sel == person_2_sel:
            st.error("Please select different people")
        else:
            try:
                shortest_path_for_graph = nx.shortest_path(graph, person_1_sel, person_2_sel)
                st.info(f"The shortest path between {person_1_sel} and {person_2_sel} is {shortest_path_for_graph}")
                subgraph = graph.subgraph(shortest_path_for_graph)
                path_graph = graphviz.Digraph()
                for node in subgraph.nodes:
                    path_graph.node(str(node))
                for edge in subgraph.edges:
                    path_graph.edge(str(edge[0]), str(edge[1]))
                st.graphviz_chart(path_graph)

            except nx.NetworkXNoPath:
                st.error(f"No path exist between {person_1_sel} and {person_2_sel}")
