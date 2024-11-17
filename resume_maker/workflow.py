import json

from agents.agent import Agent, AgentType
from typing import Dict
from agents import HeadHunterAgent, ResumeCreatorAgent, ReviewAgent


class AgentWorkflow:
    def __init__(self, model, grammar):
        self.agents: Dict[AgentType, Agent] = {}
        self.model = model
        self.history = []
        self.source = dict()
        self.grammar = grammar
        self._initialize_agents()

    def _initialize_agents(self):
        self.agents[AgentType.PLANNER] = HeadHunterAgent("Job Analyzer")
        self.agents[AgentType.EXECUTOR] = ResumeCreatorAgent("Resume Writer")
        self.agents[AgentType.REVIEWER] = ReviewAgent("Resume Reviewer")
    
    async def _execute_agent(self, agent: Agent, input: str):
        return f"Agent {agent.agent_type} executed with input {input}"
    
    def load_data(self):
        try:
            with open("./jd/hireac-99606.txt", 'r', encoding='utf-8') as f:
                self.source["job_description"] = f.read()

            with open("./stories/basic-timeline.json", "r", encoding="utf-8") as f:
                self.source["career_story"] = f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Required input file not found: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
        
    def execute(self):
        head_hunter_agent = self.agents.get(AgentType.PLANNER)
        reviewer_agent = self.agents.get(AgentType.REVIEWER)
        self.history.append({"role": "system", "content": head_hunter_agent.get_system_prompt() })
        result = dict()
        self.history.append({"role": "user", "content": head_hunter_agent.get_task_prompt("", self.source["job_description"])})
        response = self._call_llm(self.history)
        self.history.append({"role": "assistant", "content": response})
        self.history.append({"role": "user", "content": reviewer_agent.get_system_prompt()})
        print(self.history)
        response = self._call_llm(self.history)
        return response
    
    def _call_llm(self, messages):
        model_output = self.model.create_chat_completion(
            messages=messages,
            temperature=0.6,
            max_tokens=4096,
            #grammar = self.grammar
            )
        return model_output["choices"][0]["message"]["content"]

    