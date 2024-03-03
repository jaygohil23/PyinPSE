import streamlit as st
import networkx as nx
import graphviz
# from streamlit_option_menu import option_menu
import json
import uuid
from model import metamodel_dict
from graph_functions import output_node_and_edges, count_nodes, specific_node, specific_edge, \
    density, random_relation, graph_directed, graph_emptiness, shortest_path
from streamlit_agraph import agraph, Node, Edge, Config


def save_person(name, age, type_n):
    person_dict = {
        "name": name,
        "age": age,
        "ID": str(uuid.uuid4()),
        "type": type_n
    }
    if name:
        st.session_state["person_list"].append(person_dict)
        st.info("Data added Successfully")
    else:
        st.error("Enter all Fields")


def delete_person(name, age, type_n):
    for person_dict in st.session_state["person_list"]:
        if person_dict["name"] == name and person_dict["age"] == age and person_dict["type"] == type_n:
            st.session_state["person_list"].remove(person_dict)
            st.info("Data deleted Successfully")
            return
    person_not_found()


def update_person(name, age, type_n, new_name, new_age, new_type):
    for person_dict in st.session_state["person_list"]:
        if person_dict["name"] == name and person_dict["age"] == age and person_dict["type"] == type_n:
            person_dict["name"] = new_name
            person_dict["age"] = new_age
            person_dict["type"] = new_type
            st.info("Data updated Successfully")
            return
        person_not_found()


def save_relation(person1_select, relation_name, person2_select):
    if person1_select == person2_select:
        st.error("Relation can not be added to itself")
    else:
        edge_dict = {
            "Person 1": person1_select,
            "Relation": relation_name,
            "Person 2": person2_select,
            "ID": str(uuid.uuid4())
        }
        st.session_state["edge_list"].append(edge_dict)
        st.info("Relation added Successfully")


def delete_relation(person1_select, relation_name, person2_select):
    for edge_dict in st.session_state["edge_list"]:
        if edge_dict["Person 1"] == person1_select and edge_dict["Person 2"] == person2_select \
                and edge_dict["Relation"] == relation_name:
            st.session_state["edge_list"].remove(edge_dict)
            st.info("Relation deleted Successfully")
            return
    relation_not_found()


def person_not_found():
    st.info("Person not found, please store the person before removing")


def relation_not_found():
    st.info("Relation not found, please store the relation before removing")


def create_person_func():
    name_person = st.text_input("Type in your name")
    age_person = st.number_input("Type in your age", value=0)
    type_node = st.selectbox("Type", options=["Person", "Pet"])
    save_person_button = st.button("Store Person", use_container_width=True, type="primary")
    delete_person_button = st.button("Delete Person", use_container_width=True, type="secondary")
    if save_person_button:
        save_person(name_person, age_person, type_node)
    if delete_person_button:
        delete_person(name_person, age_person, type_node)
    # st.write(st.session_state["person_list"])


def import_graph_func():
    uploaded_graph = st.file_uploader("Upload an existing graph", type="json")
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        # st.write(uploaded_graph_dict)
        uploaded_nodes = uploaded_graph_dict["nodes"]
        # st.session_state["person_list"] = uploaded_nodes
        uploaded_edges = uploaded_graph_dict["edges"]
        # st.session_state["edge_list"] = uploaded_edges
        update_graph_button = st.button(
            "Update Graph via upload",
            use_container_width=True,
            type="primary"
        )

        if update_graph_button:
            st.session_state["person_list"] = uploaded_nodes
            st.session_state["edge_list"] = uploaded_edges
            graph_dict = {
                "nodes": st.session_state["person_list"],
                "edges": st.session_state["edge_list"]
            }
            st.session_state["graph_dict"] = graph_dict
            st.info("The Graph is successfully added")
    else:
        st.info("Upload the graph if available or else go ahead to the next tab")


def create_relation_func():
    person_list = st.session_state["person_list"]
    person_name_list = []
    for person in person_list:
        person_name_list.append(person["name"])

    person_1_column, relation_column, person_2_column = st.columns(3)
    with person_1_column:
        person1_select = st.selectbox(
            "Select Person 1",
            options=person_name_list,
            key="person1_select",
            index=None,
            placeholder="Person 1"
        )

    with relation_column:
        relation_list = metamodel_dict["edges"]
        relation_name = st.selectbox(
            "Specify the relation",
            options=relation_list,
            index=None,
            placeholder="Relation"
        )

    with person_2_column:
        person2_select = st.selectbox(
            "Select Person 2",
            options=person_name_list,
            key="person2_select",
            index=None,
            placeholder="Person 2"
        )
    save_relation_button = st.button("Store Relation", use_container_width=True, type="primary")
    delete_relation_button = st.button("Delete Relation", use_container_width=True, type="secondary")
    if save_relation_button:
        save_relation(person1_select, relation_name, person2_select)
    if delete_relation_button:
        delete_relation(person1_select, relation_name, person2_select)
    # st.write(f"{person1_select} is {relation_name} of {person2_select}")
    # st.write(st.session_state["edge_list"])


def store_graph_func():
    with st.expander("Show Individual List"):
        st.json(st.session_state["person_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)

    graph_dict = {
        "nodes": st.session_state["person_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict

    with st.expander("Show Graph JSON", expanded=False):
        st.json(graph_dict)


def visualize_graph_func():
    with st.expander("GraphViz Visualization"):
        graph = graphviz.Digraph()
        graph_dict = {
            "nodes": st.session_state["person_list"],
            "edges": st.session_state["edge_list"]
        }
        st.session_state["graph_dict"] = graph_dict
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]
        for node in node_list:
            node_name = node["name"]
            graph.node(node_name)
        for edge in edge_list:
            source = edge["Person 1"]
            target = edge["Person 2"]
            label = edge["Relation"]
            graph.edge(source, target, label)
        st.graphviz_chart(graph)

    with st.expander("Show Graph in AGraph"):
        graph_visualisation_nodes = []
        graph_visualisation_edges = []
        for node in st.session_state["person_list"]:
            graph_visualisation_nodes.append(
                Node(
                    id=node["name"],
                    label=node["name"],
                    size=25,
                    shape="circularImage",
                    image="https://t4.ftcdn.net/jpg/00/65/77/27/360_F_65772719_A1UV5kLi5nCEWI0BNLLiFaBPEkUbv5Fv.jpg"
                )
            )
        for edge in st.session_state["edge_list"]:
            graph_visualisation_edges.append(
                Edge(
                    source=edge["Person 1"],
                    label=edge["Relation"],
                    target=edge["Person 2"],
                )
            )
        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        hierarchical=True,
                        # **kwargs
                        )

        return_value = agraph(nodes=graph_visualisation_nodes,
                              edges=graph_visualisation_edges,
                              config=config)


def analyze_graph_func():
    G = nx.DiGraph()
    graph_dict = {
        "nodes": st.session_state["person_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    node_tuple_list = []
    edge_tuple_list = []

    for node in node_list:
        node_tuple = (node["name"], node)
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["Person 1"], edge["Person 2"], edge)
        edge_tuple_list.append(edge_tuple)

    G.add_nodes_from(node_tuple_list)
    G.add_edges_from(edge_tuple_list)

    select_function = st.selectbox(label="Select Function",
                                   options=[
                                       "Output Nodes and Edges",
                                       "Count Nodes and Edges",
                                       "Find if person exist",
                                       "Find if a direct relation exist",
                                       "Density of the graph",
                                       "Is Graph Directed?",
                                       "Is Graph Empty?",
                                       "Find if two person are somehow related",
                                       "Find the shortest path"],
                                   index=None,
                                   placeholder="What do you want to analyze?"
                                   )

    if select_function == "Output Nodes and Edges":
        if st.session_state["person_list"] == []:
            st.error("The Graph is empty")
        else:
            output_node_and_edges(graph=G)

    elif select_function == "Count Nodes and Edges":
        count_nodes(graph=G)

    elif select_function == "Find if person exist":
        if st.session_state["person_list"] == []:
            st.error("The Graph is empty")
        else:
            find_person = st.text_input("Write person's name")
            find_person_button = st.button("Find Person", type="primary")
            if find_person_button:
                specific_node(graph=G, the_node=find_person)

    elif select_function == "Find if a direct relation exist":
        # find_relation_1 = st.text_input("Person 1")
        # find_relation_2 = st.text_input("Person 2")
        person_list = st.session_state["person_list"]
        person_name_list = []
        for person in person_list:
            person_name_list.append(person["name"])
        relation_1, relation_2 = st.columns(2)
        with relation_1:
            find_relation_1 = st.selectbox(
                "Select Person 1",
                options=person_name_list,
                key="person1_select"
            )
        with relation_2:
            find_relation_2 = st.selectbox(
                "Select Person 2",
                options=person_name_list,
                key="person2_select"
            )
        find_relation_button = st.button("Find Relation", type="primary")
        if find_relation_button:
            specific_edge(graph=G, source=find_relation_1, target=find_relation_2)

    elif select_function == "Density of the graph":
        if st.session_state["person_list"] == []:
            st.error("The Graph is empty")
        else:
            density(graph=G)

    elif select_function == "Is Graph Directed?":
        if st.session_state["person_list"] == []:
            st.error("The Graph is empty")
        else:
            graph_directed(graph=G)

    elif select_function == "Is Graph Empty?":
        graph_emptiness(graph=G)

    elif select_function == "Find if two person are somehow related":
        # find_possible_relation_1 = st.text_input("Person 1")
        # find_possible_relation_2 = st.text_input("Person 2")
        person_list = st.session_state["person_list"]
        person_name_list = []
        for person in person_list:
            person_name_list.append(person["name"])

        relation_1, relation_2 = st.columns(2)
        with relation_1:
            find_possible_relation_1 = st.selectbox(
                "Select Person 1",
                options=person_name_list,
                key="person1_select"
            )
        with relation_2:
            find_possible_relation_2 = st.selectbox(
                "Select Person 2",
                options=person_name_list,
                key="person2_select"
            )

        find_possible_relation_button = st.button("Find Relation", type="primary")
        if find_possible_relation_button:
            random_relation(graph=G, source=find_possible_relation_1, target=find_possible_relation_2)

    elif select_function == "Find the shortest path":
        shortest_path(graph=G)


def export_graph_func():
    if st.session_state["person_list"] == []:
        st.error("The Graph is empty")
    else:
        graph_string = json.dumps(st.session_state["graph_dict"])
        # st.write(graph_string)
        st.download_button(
            "Export Graph to JSON",
            file_name="graph.json",
            mime="application/json",
            data=graph_string,
            use_container_width=True,
            type="primary"
        )
