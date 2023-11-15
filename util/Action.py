from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Action():
    actionType: str
    objectOn: str
    completeGoal: bool

    def __repr__(self) -> str:
        return f"""
Action: \u007b
    ActionType: {self.actionType}, 
    Object: {self.objectOn}, 
    Goal Complete: {self.completeGoal}
\u007d"""