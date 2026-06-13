import streamlit as st


def option_card(title: str, description: str, button_text: str, target_page: str):
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(description)

        if st.button(button_text, use_container_width=True):
            st.session_state.page = target_page
            st.rerun()
