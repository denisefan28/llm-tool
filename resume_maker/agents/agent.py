from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    PLANNER = "planner"
    EXECUTOR = "executor"
    REVIEWER = "reviewer"

@dataclass
class Agent:
    agent_type: AgentType
    system_prompt: str
    temperature: float = 0.3
    max_tokens: int = 4096

    def get_system_prompt(self):
        return self.system_prompt

    def get_task_prompt(self, context: str):
        return context