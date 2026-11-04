import streamlit as st
from app.models.labels import Label
from app.models.relationship import Relationship
from app.repositories.graph_repository import GraphRepository


st.set_page_config(
    page_title="Relationships",
    layout="wide"
)

st.title("Relationships")

repo = GraphRepository()

try:

    # ---------------------------------------------------------
    # Retrieve Technologies and Relationships
    # ---------------------------------------------------------

    technologies = repo.get_all_nodes(Label.TECHNOLOGY)

    technology_names = [
        technology["node"]["name"]
        for technology in technologies
    ]

    relationships = repo.get_all_relationships(
        Label.TECHNOLOGY,
        Label.TECHNOLOGY
    )

    relationship_types = list(Relationship)

    # ---------------------------------------------------------
    # Create Relationship
    # ---------------------------------------------------------

    st.subheader("Create Relationship")

    if len(technology_names) >= 2:

        with st.form("create_relationship_form"):

            source = st.selectbox(
                "Source Technology",
                technology_names,
                key="create_source"
            )

            relationship_type = st.selectbox(
                "Relationship Type",
                relationship_types,
                format_func=lambda r: r.value,
                key="create_type"
            )

            target = st.selectbox(
                "Target Technology",
                technology_names,
                key="create_target"
            )

            create_submitted = st.form_submit_button(
                "Create Relationship"
            )

            if create_submitted:

                if source == target:

                    st.error(
                        "Source and target must be different technologies."
                    )

                else:

                    result = repo.create_relationship(
                        Label.TECHNOLOGY,
                        source,
                        relationship_type,
                        Label.TECHNOLOGY,
                        target
                    )

                    if result:

                        st.success(
                            f"{source} → {relationship_type.value} → {target} created."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Could not create relationship. "
                            "Check that both technologies exist."
                        )

    else:

        st.info(
            "Add at least two technologies before creating relationships."
        )

    st.divider()

    # ---------------------------------------------------------
    # Edit Relationship
    # ---------------------------------------------------------

    st.subheader("Edit Relationship")

    if relationships:

        def relationship_label(item):

            return (
                f"{item['source']} → "
                f"{item['relationship']} → "
                f"{item['target']}"
            )

        with st.form("edit_relationship_form"):

            selected_old = st.selectbox(
                "Select Existing Relationship",
                relationships,
                format_func=relationship_label,
                key="edit_existing"
            )

            st.caption(
                "Select the replacement source, relationship type and target."
            )

            new_source = st.selectbox(
                "New Source Technology",
                technology_names,
                index=technology_names.index(
                    selected_old["source"]
                ),
                key="edit_source"
            )

            new_relationship = st.selectbox(
                "New Relationship Type",
                relationship_types,
                index=[
                    r.value for r in relationship_types
                ].index(selected_old["relationship"]),
                format_func=lambda r: r.value,
                key="edit_type"
            )

            new_target = st.selectbox(
                "New Target Technology",
                technology_names,
                index=technology_names.index(
                    selected_old["target"]
                ),
                key="edit_target"
            )

            edit_submitted = st.form_submit_button(
                "Update Relationship"
            )

            if edit_submitted:

                if new_source == new_target:

                    st.error(
                        "Source and target must be different technologies."
                    )

                else:

                    result = repo.update_relationship(
                        source_label=Label.TECHNOLOGY,
                        old_source=selected_old["source"],
                        old_relationship=Relationship(
                            selected_old["relationship"]
                        ),
                        old_target=selected_old["target"],
                        new_source=new_source,
                        new_relationship=new_relationship,
                        new_target=new_target,
                        target_label=Label.TECHNOLOGY
                    )

                    if result:

                        st.success(
                            "Relationship updated successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Relationship could not be updated."
                        )

    else:

        st.info("No relationships available to edit.")

    st.divider()

    # ---------------------------------------------------------
    # Delete Relationship
    # ---------------------------------------------------------

    st.subheader("Delete Relationship")

    if relationships:

        with st.form("delete_relationship_form"):

            selected_delete = st.selectbox(
                "Select Relationship to Delete",
                relationships,
                format_func=relationship_label,
                key="delete_relationship"
            )


            delete_submitted = st.form_submit_button(
                "Delete Relationship"
            )

            if delete_submitted:

                result = repo.delete_relationship(
                    Label.TECHNOLOGY,
                    selected_delete["source"],
                    Relationship(selected_delete["relationship"]),
                    Label.TECHNOLOGY,
                    selected_delete["target"]
                )

                st.success(
                    "Relationship deleted successfully."
                )

                st.rerun()

    else:

        st.info("No relationships available to delete.")

    st.divider()

    # ---------------------------------------------------------
    # Display Existing Relationships
    # ---------------------------------------------------------

    st.subheader("Available Relationships")

    current_relationships = repo.get_all_relationships(
        Label.TECHNOLOGY,
        Label.TECHNOLOGY
    )

    if current_relationships:

        rows = [
            {
                "Source": r["source"],
                "Relationship": r["relationship"],
                "Target": r["target"]
            }
            for r in current_relationships
        ]

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No relationships found.")

finally:

    repo.close()
