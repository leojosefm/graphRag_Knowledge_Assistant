import streamlit as st

from models.labels import Label
from models.technology_category import TechnologyCategory
from repositories.graph_repository import GraphRepository


st.set_page_config(
    page_title="Technologies",
    layout="wide"
)

st.title("Technologies")

repo = GraphRepository()

# ---------------------------------------------------------
# Add Technology
# ---------------------------------------------------------

st.subheader("Add Technology")

with st.form("technology_form"):

    name = st.text_input("Technology Name")

    category = st.selectbox(
        "Category",
        options=list(TechnologyCategory),
        format_func=lambda c: c.value
    )

    description = st.text_area("Description")

    submitted = st.form_submit_button("Save")

    if submitted:

        if not name.strip():

            st.error("Technology Name is required.")

        else:

            repo.create_node(
                label=Label.TECHNOLOGY,
                properties={
                    "name": name.strip(),
                    "category": category.value,
                    "description": description.strip()
                }
            )

            st.success(f"'{name}' has been added.")

            st.rerun()

# ---------------------------------------------------------
# Existing Technologies
# ---------------------------------------------------------

st.divider()

st.subheader("Available Technologies")

technologies = repo.get_all_nodes(Label.TECHNOLOGY)

if technologies:

    rows = []

    for technology in technologies:

        node = technology["node"]

        rows.append(
            {
                "Name": node.get("name"),
                "Category": node.get("category"),
                "Description": node.get("description")
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No technologies found.")

repo.close()