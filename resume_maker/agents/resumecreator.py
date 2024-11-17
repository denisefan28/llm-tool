from .agent import Agent


class ResumeCreatorAgent(Agent):
    def __init__(self, name: str):
        self.name = name
        self.system_prompt = """You are a professional resume writer, who will develop tailored and polished resume based on people's past experience. You make sure the resume highly aligned with the job descirption."""

    def get_experience_create_prompt(self, experience: str):
        return f"Write a keyword optimized experience for specific job based on the job description provided. For the bullet points, ensure description is clear with quantified achievements if necessary. '{experience}'"
    
    def get_skills_prompt(self, content: str):
        return f"Create a skill section based on provided past experience. '{content}'"