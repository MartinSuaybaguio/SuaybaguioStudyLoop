import html
import streamlit as st


class BaseView:
    """Abstract parent of every screen (MVC: View)."""
    def __init__(self, service):
        self.s = service

    def render(self):
        raise NotImplementedError

    def flash(self):
        r = st.session_state.pop("flash", None)
        if r:
            st.success(f"Nice work! You earned {r.points} points.")
            for b in r.badges:
                st.info(f"Badge unlocked: {b.name}. {b.description}")
            if r.goal_done:
                st.balloons()

    def finish(self, goal_id, step_id=None):
        st.session_state["flash"] = self.s.finish_step(goal_id, step_id) if step_id else self.s.finish_goal(goal_id)
        st.rerun()

    @staticmethod
    def tag(text: str, hot: bool = False) -> str:
        return f'<span class="sl-tag{" hot" if hot else ""}">{html.escape(text)}</span>'
