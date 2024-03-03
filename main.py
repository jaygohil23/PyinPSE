import streamlit as st
# from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_option_menu import option_menu
from tabs import import_graph_func, create_person_func, create_relation_func, store_graph_func, \
    visualize_graph_func, analyze_graph_func, export_graph_func

if __name__ == '__main__':
    if "person_list" not in st.session_state:
        st.session_state["person_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []

    tab_list = ["Import the Graph",
                "Create People",
                "Create relations between Persons",
                "Store the graph",
                "Visualize the Graph",
                "Analyze the Graph",
                "Export the Graph"
                ]

    st.title('Graph Analyzer')
    with st.sidebar:
        selected_tab = option_menu("Main Menu", options=tab_list,

                                   icons=['upload', 'person-plus-fill', 'people-fill',
                                          'cart-check-fill', 'eye-fill', 'clipboard2-pulse-fill', 'download'],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical"
                                   )
        # st.write(selected)

    if selected_tab == "Import the Graph":
        import_graph_func()

    if selected_tab == "Create People":
        create_person_func()

    if selected_tab == "Create relations between Persons":
        create_relation_func()

    if selected_tab == "Store the graph":
        store_graph_func()

    if selected_tab == "Visualize the Graph":
        visualize_graph_func()

    if selected_tab == "Analyze the Graph":
        analyze_graph_func()

    if selected_tab == "Export the Graph":
        export_graph_func()
