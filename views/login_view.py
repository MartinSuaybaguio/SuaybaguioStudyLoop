import streamlit as st
from views.base_view import BaseView


class LoginView(BaseView):
    def __init__(self, auth):
        super().__init__(None)
        self.auth = auth

    def render(self):
        st.title("Study Loop")
        st.write("Turn your schoolwork into Daily Missions, earn points, and keep your streak going.")
        login, signup = st.tabs(["Log in", "Create profile"])
        with login:
            with st.form("login"):
                n, p = st.text_input("Name"), st.text_input("Password", type="password")
                if st.form_submit_button("Log in"):
                    self._go(self.auth.login, n, p)
        with signup:
            with st.form("signup"):
                n, p = st.text_input("Choose a name"), st.text_input("Choose a password", type="password")
                if st.form_submit_button("Create profile"):
                    self._go(self.auth.register, n, p)

    @staticmethod
    def _go(action, n, p):
        try:
            st.session_state["user"] = action(n, p)
            st.rerun()
        except ValueError as e:
            st.error(str(e))
