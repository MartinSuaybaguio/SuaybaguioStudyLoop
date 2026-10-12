from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass(frozen=True)
class Achievement:
    key: str
    name: str
    description: str


ACHIEVEMENTS = [
    Achievement("project_starter", "Project Starter", "Start working on a major project."),
    Achievement("deadline_hero", "Deadline Hero", "Complete a task before its deadline."),
    Achievement("streak_master", "Study Streak Master", "Keep a study streak going for 3 days."),
    Achievement("task_crusher", "Task Crusher", "Complete 3 tasks in one day."),
    Achievement("goal_getter", "Goal Getter", "Complete an entire goal."),
]


@dataclass
class Reward:
    points: int = 0
    goal_done: bool = False
    badges: list = field(default_factory=list)


class GamificationEngine:
    RULES = {
        "project_starter": lambda p, iso: p.started_project,
        "deadline_hero": lambda p, iso: p.deadline_wins >= 1,
        "streak_master": lambda p, iso: p.best_streak >= 3,
        "task_crusher": lambda p, iso: p.daily_done.get(iso, 0) >= 3,
        "goal_getter": lambda p, iso: p.goals_done >= 1,
    }

    def award(self, profile, goal, today: date, goal_done: bool) -> Reward:
        lvl = {"Easy": 1, "Medium": 2, "Hard": 3}[goal.difficulty]
        pts = 10 + 5 * lvl + goal.minutes_per_step() // 15
        if today <= goal.due:
            pts += 10
            profile.deadline_wins += 1
        if goal_done:
            pts += 25 * lvl
            profile.goals_done += 1
        iso = today.isoformat()
        if profile.last_active != iso:
            yesterday = (today - timedelta(days=1)).isoformat()
            profile.streak = profile.streak + 1 if profile.last_active == yesterday else 1
            profile.last_active = iso
        profile.best_streak = max(profile.best_streak, profile.streak)
        profile.daily_done[iso] = profile.daily_done.get(iso, 0) + 1
        profile.points += pts
        if goal.kind == "Project":
            profile.started_project = True
        new = [a for a in ACHIEVEMENTS if a.key not in profile.achievements and self.RULES[a.key](profile, iso)]
        profile.achievements += [a.key for a in new]
        return Reward(pts, goal_done, new)
