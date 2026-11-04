import streamlit as st

from app.models.labels import Label
from app.models.technology_category import TechnologyCategory
from app.repositories.graph_repository import GraphRepository


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

technologies = repo.get_all_nodes(Label.TECHNOLOGY)

st.subheader("Delete Technology")

if technologies:

    technology_names = [
        technology["node"]["name"]
        for technology in technologies
    ]

    selected_technology = st.selectbox(
        "Select technology to delete",
        technology_names
    )

    confirm_delete = st.checkbox(
        f"I understand that deleting {selected_technology} "
        "will also delete its relationships."
    )

    if st.button(
        "Delete Technology",
        disabled=not confirm_delete
    ):
        try:
            repo.delete_node(
                Label.TECHNOLOGY,
                selected_technology
            )

            st.success(
                f"{selected_technology} deleted successfully."
            )

            st.rerun()

        except Exception as e:
            st.error(f"Unable to delete technology: {e}")

else:
    st.info("No technologies available to delete.")

st.subheader("Available Technologies")

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