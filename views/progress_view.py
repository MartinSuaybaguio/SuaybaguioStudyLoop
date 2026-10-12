from datetime import timedelta
import streamlit as st
from services.gamification import ACHIEVEMENTS
from views.base_view import BaseView


class ProgressView(BaseView):
    def render(self):
        s, p = self.s, self.s.profile
        st.title("Progress")
        a, b, c, d = st.columns(4)
        a.metric("Points", p.points)
        b.metric("Level", p.level)
        c.metric("Current streak", f"🔥 {s.streak()}")
        d.metric("Best streak", f"🔥 {p.best_streak}")
        st.subheader("Tasks finished, last 7 days")
        days = [s.today - timedelta(days=i) for i in range(6, -1, -1)]
        st.bar_chart({d.strftime("%a %d"): p.daily_done.get(d.isoformat(), 0) for d in days}, color="#1E6FEB")
        st.subheader("Achievements")
        cols = st.columns(2)
        for i, ach in enumerate(ACHIEVEMENTS):
            got = ach.key in p.achievements
            cols[i % 2].markdown(
                f'<div class="sl-badge{"" if got else " locked"}"><b>{ach.name}</b>{ach.description}<br>'
                f'{"Unlocked" if got else "Locked"}</div>', unsafe_allow_html=True)
        st.subheader("Remaining work")
        st.write(f"{len(s.active())} active goals, {s.remaining_steps()} tasks left, {len(s.completed())} goals completed.")
