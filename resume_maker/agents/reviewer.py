from .agent import Agent


class ReviewAgent(Agent):
    def __init__(self, name: str):
        self.system_prompt = "As a resume reviewer, make sure the response return in json format. If not, corret and return it in json format, which only contains 'title', 'responsibility', 'requirements'"

    def get_experience_review(self):
        return "As a resume reviewer, make sure the response only contains bullet points, remove non bullet points text, response without opening words, such as, 'Here is the rewritten response:'"