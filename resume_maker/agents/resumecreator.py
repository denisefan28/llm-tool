from .agent import Agent


class ResumeCreatorAgent(Agent):
    def __init__(self, name: str):
        self.name = name
        self.system_prompt = """You are a professional resume writer, who will develop tailored and polished resume based on people's past experience. You make sure the resume highly aligned with the job descirption."""

    def get_task_prompt(self, **args):
        prompt_template = "Generate work experience as a {title} at {company}. Response only in one paragraph without header. The experience generated based on the following content: '{career_story}'"
        prompt_text = prompt_template.format(
            title = args.get("title", "N/A"),
            company = args.get("company", "N/A"),
            start = args.get("start", "N/A"),
            end = args.get("end", "N/A"),
            career_story = args.get("story", "N/A")
        )
        return prompt_text

    def get_experience_create_prompt(self, job: str):
        return f"Write a keyword optimized experience for specific job based on the job description provided. Response only in three to five bullet points, ensure description is clear with quantified achievements if necessary. Don't make up quantified data! Job Description '{job}'"
    
    def get_skills_prompt(self, content: str, jd: str):
        return f"Create a skill section based on provided past experience. '{content}' aligned with job descipriton {jd}"