from __future__ import annotations
import uuid
from dataclasses import dataclass, field, asdict
from datetime import date

DIFFICULTY = {"Easy": 1, "Medium": 2, "Hard": 3}
KINDS = ["Assignment", "Project", "Quiz", "Exam", "Other"]


def new_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class Subtask:
    title: str
    id: str = field(default_factory=new_id)
    done: bool = False
    completed_on: str = ""


@dataclass
class Goal:
    title: str
    subject: str
    kind: str
    deadline: str  # ISO date
    difficulty: str
    minutes: int
    subtasks: list = field(default_factory=list)
    id: str = field(default_factory=new_id)
    done: bool = False
    completed_on: str = ""
    created_on: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def due(self) -> date:
        return date.fromisoformat(self.deadline)

    def days_left(self, today: date) -> int:
        return (self.due - today).days

    def due_label(self, today: date) -> str:
        d = self.days_left(today)
        if d < 0:
            return f"Overdue by {-d} day{'s' if d != -1 else ''}"
        return "Due today" if d == 0 else "Due tomorrow" if d == 1 else f"Due in {d} days"

    @property
    def progress(self) -> float:
        if self.done:
            return 1.0
        if not self.subtasks:
            return 0.0
        return sum(s.done for s in self.subtasks) / len(self.subtasks)

    def open_steps(self) -> list:
        return [s for s in self.subtasks if not s.done]

    def minutes_per_step(self) -> int:
        return max(5, self.minutes // max(1, len(self.subtasks)))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Goal":
        d = dict(d)
        d["subtasks"] = [Subtask(**s) for s in d.get("subtasks", [])]
        return cls(**d)
