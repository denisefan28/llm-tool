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
        writer_agent = self.agents.get(AgentType.EXECUTOR)
        self.history.append({"role": "system", "content": head_hunter_agent.get_system_prompt() })
        self.history.append({"role": "user", "content": head_hunter_agent.get_task_prompt("", self.source["job_description"])})
        job_description_response = self._call_llm(self.history)
        self.history.append({"role": "assistant", "content": job_description_response})
        self.history.append({"role": "user", "content": reviewer_agent.get_system_prompt()})
        job_requirements_json = self._call_llm(self.history)

        self._reset_history()
        self.history.append({"role": "system", "content": writer_agent.get_system_prompt() })
        career_details = json.loads(self.source["career_story"])
        updated_career = []
        for k in career_details.get("basic"):
            messages = self.history
            messages.append({"role": "user", "content": writer_agent.get_task_prompt(**k)})
            concise_experience = self._call_llm(messages)
            messages.append({"role": "assistance", "content": concise_experience})
            messages.append({"role": "user", "content": writer_agent.get_experience_create_prompt(job_requirements_json)})
            optimised_experience = self._call_llm(messages)
            messages.append({"role": "assistance", "content": optimised_experience})
            messages.append({"role": "user", "content": reviewer_agent.get_experience_review()})
            reviewed_experience = self._call_llm(messages)

            print("!!! reviewed experience\n", reviewed_experience) 
            k["experience"] = reviewed_experience
            updated_career.append(k)
        return updated_career

    def _call_llm(self, messages):
        model_output = self.model.create_chat_completion(
            messages=messages,
            temperature=0.6,
            max_tokens=4096,
            #grammar = self.grammar
            )
        return model_output["choices"][0]["message"]["content"]
    
    def _reset_history(self):
        self.history = []

    