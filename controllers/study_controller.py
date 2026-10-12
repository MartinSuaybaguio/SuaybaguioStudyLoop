from dataclasses import asdict
from datetime import date, timedelta
from models.goal import Goal, Subtask
from models.profile import Profile
from services.planner import Planner
from services.gamification import GamificationEngine, Reward

SUGGESTED_STEPS = {
    "Project": ["Complete research", "Write introduction", "Add references", "Review final draft"],
    "Assignment": ["Read the instructions", "Work on the answers", "Proofread and submit"],
    "Quiz": ["Review notes", "Practice questions", "Final recap"],
    "Exam": ["List topics to cover", "Study each topic", "Take a practice test", "Final review"],
}


class StudyController:
    def __init__(self, storage, name: str, planner=None, engine=None):
        self.storage, self.key = storage, name
        self.record = storage.load(name)
        self.name = self.record["name"]
        self.profile = Profile(**self.record["profile"])
        self.goals = [Goal.from_dict(g) for g in self.record["goals"]]
        self.planner = planner or Planner()
        self.engine = engine or GamificationEngine()

    # persistence
    def save(self) -> None:
        self.record["profile"] = asdict(self.profile)
        self.record["goals"] = [g.to_dict() for g in self.goals]
        self.storage.save(self.key, self.record)

    # queries
    @property
    def today(self) -> date:
        return date.today()

    def find(self, goal_id: str) -> Goal:
        return next(g for g in self.goals if g.id == goal_id)

    def active(self) -> list:
        return sorted((g for g in self.goals if not g.done), key=lambda g: g.deadline)

    def completed(self) -> list:
        return [g for g in self.goals if g.done]

    def missions(self) -> list:
        return self.planner.build(self.active(), self.today)

    def done_today(self) -> list:
        iso = self.today.isoformat()
        out = []
        for g in self.goals:
            out += [f"{g.title}: {s.title}" for s in g.subtasks if s.completed_on == iso]
            if g.done and g.completed_on == iso and not g.subtasks:
                out.append(g.title)
        return out

    def streak(self) -> int:
        last = self.profile.last_active
        ok = last in (self.today.isoformat(), (self.today - timedelta(days=1)).isoformat())
        return self.profile.streak if ok else 0

    def remaining_steps(self) -> int:
        return sum(len(g.open_steps()) if g.subtasks else 1 for g in self.active())

    # commands
    def add_goal(self, title, subject, kind, deadline, difficulty, minutes, steps, suggest=False) -> Goal:
        title, subject = title.strip(), subject.strip()
        if not title or not subject:
            raise ValueError("Enter a title and a subject.")
        titles = [s.strip() for s in steps if s.strip()]
        if not titles and suggest:
            titles = SUGGESTED_STEPS.get(kind, [])
        goal = Goal(title, subject, kind, deadline.isoformat(), difficulty, int(minutes),
                    [Subtask(t) for t in titles])
        self.goals.append(goal)
        self.save()
        return goal

    def add_step(self, goal_id: str, title: str) -> None:
        if title.strip():
            self.find(goal_id).subtasks.append(Subtask(title.strip()))
            self.save()

    def finish_step(self, goal_id: str, step_id: str) -> Reward:
        goal = self.find(goal_id)
        step = next(s for s in goal.subtasks if s.id == step_id)
        step.done, step.completed_on = True, self.today.isoformat()
        all_done = not goal.open_steps()
        if all_done:
            goal.done, goal.completed_on = True, self.today.isoformat()
        reward = self.engine.award(self.profile, goal, self.today, all_done)
        self.save()
        return reward

    def finish_goal(self, goal_id: str) -> Reward:
        goal = self.find(goal_id)
        iso = self.today.isoformat()
        for s in goal.open_steps():
            s.done, s.completed_on = True, iso
        goal.done, goal.completed_on = True, iso
        reward = self.engine.award(self.profile, goal, self.today, True)
        self.save()
        return reward

    def delete_goal(self, goal_id: str) -> None:
        self.goals = [g for g in self.goals if g.id != goal_id]
        self.save()
