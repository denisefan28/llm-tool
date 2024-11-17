from .agent import Agent


class HeadHunterAgent(Agent):
    def __init__(self, name: str):
        self.name = name
        self.keys = ["Title", "Responsibilities", "Must Have Skills", "Nice to Have Skills"]
        self.system_prompt = "You act as a professional headhunter with over 10 years experience. You are responsible for analysing the job description."

    def get_task_prompt(self, query: str, context: str):
        return f"Read the below job description. Firstly Identify if it is an internship/co-op opportunity or not. Secondly check if it is a part time or full time opportunity. Full-time employees typically work 37.5 to 40 hours per week, while part-time employees work fewer hours, often less than 30 hours per week. If the job is a co-op position without specify the working hours, it is a full time job for students. JD: {context}"
        #return f"Based on the below job description. What is the {query} of the position? {context}"