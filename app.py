import streamlit as st
from services.storage import Storage
from services.auth_service import AuthService
from controllers.study_controller import StudyController
from views import VIEWS
from views.login_view import LoginView
from views.theme import Theme

st.set_page_config(page_title="Study Loop", page_icon=":material/loop:", layout="wide")
Theme.apply()


@st.cache_resource
def get_storage() -> Storage:
    return Storage()


storage = get_storage()
name = st.session_state.get("user")
if not name or not storage.exists(name):
    LoginView(AuthService(storage)).render()
    st.stop()

controller = StudyController(storage, name)
with st.sidebar:
    st.markdown("## Study Loop")
    st.caption(f"Signed in as {controller.name}")
    choice = st.radio("Go to", list(VIEWS), label_visibility="collapsed")
    if st.button("Log out"):
        del st.session_state["user"]
        st.rerun()
VIEWS[choice](controller).render()
