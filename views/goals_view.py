import streamlit as st
from views.base_view import BaseView


class GoalsView(BaseView):
    def render(self):
        s = self.s
        self.flash()
        st.title("My goals")
        active, done = st.tabs(["Active", "Completed"])
        with active:
            if not s.active():
                st.info("No active goals. Add one from the sidebar.")
            for g in s.active():
                with st.expander(f"{g.title} ({g.subject}), {int(g.progress * 100)}% done"):
                    st.caption(f"{g.kind}, {g.difficulty}, {g.minutes} min, {g.due_label(s.today).lower()} ({g.due:%b %d})")
                    st.progress(g.progress)
                    for step in g.subtasks:
                        l, r = st.columns([5, 1], vertical_alignment="center")
                        l.markdown(f"~~{step.title}~~" if step.done else step.title)
                        if not step.done and r.button("Finish", key=f"fs_{step.id}"):
                            self.finish(g.id, step.id)
                    with st.form(f"as_{g.id}", clear_on_submit=True):
                        new = st.text_input("Add a step", key=f"ns_{g.id}")
                        if st.form_submit_button("Add step") and new.strip():
                            s.add_step(g.id, new)
                            st.rerun()
                    a, b = st.columns(2)
                    if a.button("Complete whole goal", key=f"cg_{g.id}"):
                        self.finish(g.id)
                    if b.button("Delete goal", key=f"dg_{g.id}"):
                        s.delete_goal(g.id)
                        st.rerun()
        with done:
            if not s.completed():
                st.caption("Completed goals show up here.")
            for g in s.completed():
                st.markdown(f"- **{g.title}** ({g.subject}), finished {g.completed_on}")
