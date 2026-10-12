from dataclasses import dataclass, field


@dataclass
class Profile:
    points: int = 0
    streak: int = 0
    best_streak: int = 0
    last_active: str = ""
    achievements: list = field(default_factory=list)
    daily_done: dict = field(default_factory=dict)
    deadline_wins: int = 0
    goals_done: int = 0
    started_project: bool = False

    @property
    def level(self) -> int:
        return self.points // 100 + 1
