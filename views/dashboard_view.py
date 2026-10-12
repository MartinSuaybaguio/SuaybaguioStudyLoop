import html
import streamlit as st
from views.base_view import BaseView


class DashboardView(BaseView):
    def render(self):
        s, p = self.s, self.s.profile
        self.flash()
        st.title(f"Hi, {s.name}")
        a, b, c, d = st.columns(4)
        a.metric("Points", p.points)
        b.metric("Level", p.level)
        c.metric("Study streak", f"🔥 {s.streak()} day{'s' if s.streak() != 1 else ''}")
        d.metric("Tasks left", s.remaining_steps())
        st.progress((p.points % 100) / 100, text=f"{100 - p.points % 100} points to level {p.level + 1}")

        st.subheader("Daily Missions")
        missions = s.missions()
        if not missions:
            st.info("No missions right now. Add a goal to get started.")
        else:
            st.caption(f"{len(missions)} missions, about {sum(m.minutes for m in missions)} minutes")
        for m in missions:
            with st.container(border=True):
                left, right = st.columns([5, 1], vertical_alignment="center")
                left.markdown(f"**{html.escape(m.title)}**")
                left.markdown(self.tag(m.goal.subject) + self.tag(f"{m.minutes} min") + self.tag(m.goal.difficulty)
                              + self.tag(m.reason, hot=m.goal.days_left(s.today) <= 1), unsafe_allow_html=True)
                if right.button("Finish", key=f"m_{m.goal.id}_{m.step.id if m.step else 'g'}"):
                    self.finish(m.goal.id, m.step.id if m.step else None)

        done = s.done_today()
        if done:
            st.subheader("Finished today")
            for t in done:
                st.markdown(f"- {t}")

        st.subheader("Upcoming deadlines")
        goals = s.active()[:5]
        if not goals:
            st.caption("Nothing due.")
        for g in goals:
            st.markdown(f"**{g.title}** ({g.subject}) due {g.due.strftime('%b %d')}, {g.due_label(s.today).lower()}")
            st.progress(g.progress)
