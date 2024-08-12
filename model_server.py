from flask import Flask, request
from llama_cpp import Llama
import json

app = Flask(__name__)
LLM = Llama(model_path="./model/codellama-13b-instruct.Q4_K_M.gguf")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/prompt", methods=["POST"])
def prompt_model():
    LLM_output = "unknown"
    if request.method == "POST":
        json_data = request.json
        prompt_txt = json_data.get("prompt", "hi")
        print("prompt_txt: ", prompt_txt, json_data)
        LLM_output = LLM(prompt_txt)
        response_txt = LLM_output["choices"][0]["text"]
        LLM_output = response_txt.split("\n")[0]
    return {"response": LLM_output}

