from datetime import timedelta
import streamlit as st
from models.goal import KINDS, DIFFICULTY
from views.base_view import BaseView


class AddGoalView(BaseView):
    def render(self):
        st.title("Add a goal")
        st.caption("Add an assignment, quiz, project, or exam. Break big goals into steps, one per line.")
        with st.form("add_goal", clear_on_submit=True):
            title = st.text_input("Goal", placeholder="Finish Science Project")
            c1, c2 = st.columns(2)
            subject = c1.text_input("Subject", placeholder="Science")
            kind = c2.selectbox("Type", KINDS, index=1)
            c3, c4, c5 = st.columns(3)
            deadline = c3.date_input("Deadline", min_value=self.s.today, value=self.s.today + timedelta(days=7))
            difficulty = c4.selectbox("Difficulty", list(DIFFICULTY), index=1)
            minutes = c5.number_input("Estimated minutes (total)", 5, 3000, 90, step=5)
            steps = st.text_area("Steps (one per line)", placeholder="Complete research\nWrite introduction\nAdd references\nReview final draft")
            suggest = st.checkbox("Suggest steps if I leave this empty", value=True)
            if st.form_submit_button("Save goal"):
                try:
                    g = self.s.add_goal(title, subject, kind, deadline, difficulty, minutes, steps.splitlines(), suggest)
                    st.success(f"Saved \"{g.title}\" with {len(g.subtasks)} steps. Check your Daily Missions.")
                except ValueError as e:
                    st.error(str(e))
