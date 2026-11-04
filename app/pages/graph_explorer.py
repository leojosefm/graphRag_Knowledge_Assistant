
import html

import streamlit as st
import streamlit.components.v1 as components

from pyvis.network import Network

from app.models.labels import Label
from app.repositories.graph_repository import GraphRepository


st.set_page_config(
    page_title="Graph Explorer",
    layout="wide"
)

st.title("Graph Explorer")
st.caption("Explore technologies and their relationships stored in Neo4j.")


repo = GraphRepository()

try:
    # --------------------------------------------------
    # 1. Retrieve graph data from Neo4j
    # --------------------------------------------------

    technology_records = repo.get_all_nodes(Label.TECHNOLOGY)

    technologies = [
        record["node"]
        for record in technology_records
        if record.get("node") and record["node"].get("name")
    ]

    relationships = repo.get_all_relationships(
        Label.TECHNOLOGY,
        Label.TECHNOLOGY
    )

finally:
    repo.close()


# ------------------------------------------------------
# 2. Check whether graph data exists
# ------------------------------------------------------

if not technologies:

    st.info("No technologies found. Add technologies first.")

    st.stop()


# ------------------------------------------------------
# 3. Graph filters
# ------------------------------------------------------

categories = sorted({
    technology.get("category", "Uncategorized")
    for technology in technologies
})

technology_names = sorted([
    technology["name"]
    for technology in technologies
])

col1, col2 = st.columns(2)

with col1:
    selected_categories = st.multiselect(
        "Filter by category",
        options=categories,
        default=categories
    )

filtered_technologies = [
    technology
    for technology in technologies
    if technology.get("category", "Uncategorized")
    in selected_categories
]

filtered_names = {
    technology["name"]
    for technology in filtered_technologies
}

with col2:
    focus_options = ["All technologies"] + sorted(filtered_names)

    selected_focus = st.selectbox(
        "Explore a technology and its direct neighbours",
        options=focus_options
    )


# ------------------------------------------------------
# 4. Apply focus filter
# ------------------------------------------------------

if selected_focus != "All technologies":

    visible_names = {selected_focus}

    for relationship in relationships:

        source = relationship["source"]
        target = relationship["target"]

        if source == selected_focus:
            visible_names.add(target)

        if target == selected_focus:
            visible_names.add(source)

    filtered_technologies = [
        technology
        for technology in filtered_technologies
        if technology["name"] in visible_names
    ]

visible_names = {
    technology["name"]
    for technology in filtered_technologies
}


# ------------------------------------------------------
# 5. Build interactive graph
# ------------------------------------------------------

graph = Network(
    height="700px",
    width="100%",
    directed=True,
    bgcolor="#FFFFFF",
    font_color="#222222",
    cdn_resources="in_line"
)

# Enable interactive physics
graph.toggle_physics(True)

# Add nodes
for technology in filtered_technologies:

    name = technology["name"]
    category = technology.get("category", "Uncategorized")
    description = technology.get("description", "")

    tooltip = (
        f"<b>{html.escape(name)}</b><br>"
        f"Category: {html.escape(category)}<br>"
        f"{html.escape(description)}"
    )

    graph.add_node(
        name,
        label=name,
        title=tooltip,
        group=category,
        size=25
    )


# Add relationships as directed edges
for relationship in relationships:

    source = relationship["source"]
    target = relationship["target"]
    relationship_type = relationship["relationship"]

    # Only show edges where both nodes are visible
    if source in visible_names and target in visible_names:

        graph.add_edge(
            source,
            target,
            label=relationship_type,
            title=relationship_type,
            arrows="to"
        )


# ------------------------------------------------------
# 6. Display graph statistics
# ------------------------------------------------------

visible_relationships = [
    relationship
    for relationship in relationships
    if relationship["source"] in visible_names
    and relationship["target"] in visible_names
]

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Technologies",
    len(filtered_technologies)
)

metric2.metric(
    "Relationships",
    len(visible_relationships)
)

metric3.metric(
    "Categories",
    len({
        technology.get("category", "Uncategorized")
        for technology in filtered_technologies
    })
)


# ------------------------------------------------------
# 7. Render graph in Streamlit
# ------------------------------------------------------

st.divider()

if filtered_technologies:

    graph_html = graph.generate_html()

    components.html(
        graph_html,
        height=750,
        scrolling=True
    )

else:

    st.info("No technologies match the selected filters.")
