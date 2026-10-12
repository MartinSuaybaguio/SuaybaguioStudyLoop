from dataclasses import dataclass
from datetime import date
from typing import Optional
from models.goal import Goal, Subtask, DIFFICULTY


@dataclass
class Mission:
    goal: Goal
    step: Optional[Subtask]
    minutes: int
    score: float
    reason: str

    @property
    def title(self) -> str:
        return f"{self.goal.title}: {self.step.title}" if self.step else self.goal.title


class Planner:
    def __init__(self, daily_minutes: int = 120, max_missions: int = 6):
        self.daily_minutes = daily_minutes
        self.max_missions = max_missions

    @staticmethod
    def score(goal: Goal, today: date) -> float:
        d = goal.days_left(today)
        urgency = 60 if d < 0 else 40 / (d + 1) + (20 if d <= 1 else 0)
        difficulty = 4 * DIFFICULTY[goal.difficulty]
        effort = min(goal.minutes / 30, 6)
        unfinished = (1 - goal.progress) * 10
        return urgency + difficulty + effort + unfinished

    def build(self, goals: list, today: date) -> list:
        ranked = sorted((g for g in goals if not g.done), key=lambda g: -self.score(g, today))
        missions, used = [], 0
        for g in ranked:
            steps = g.open_steps() or [None]
            take = 2 if g.days_left(today) <= 2 and len(steps) > 1 else 1
            for step in steps[:take]:
                mins = g.minutes_per_step() if step else g.minutes
                if missions and (used + mins > self.daily_minutes or len(missions) >= self.max_missions):
                    return missions
                missions.append(Mission(g, step, mins, self.score(g, today), g.due_label(today)))
                used += mins
        return missions
