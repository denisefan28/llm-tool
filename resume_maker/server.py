from flask import Flask, request, session
from llama_cpp import Llama
from datetime import timedelta
from config.secretmanager import SecretManager
from workflow import AgentWorkflow
from llama_cpp.llama import Llama, LlamaGrammar


grammar = None
with open('./config/json_grammar.gbnf') as f:
    grammar_text = f.read()
    grammar = LlamaGrammar.from_string(grammar_text)

secret_manager = SecretManager()

app = Flask(__name__)
LLM = Llama(
    model_path="../models/llama3.2/Llama-3.2-1B-Instruct-Q3_K_XL.gguf",
    chat_format="llama-3",
    return_full_text=True,
    n_ctx=4096,
    grammar = grammar
    )

app.secret_key = secret_manager.get_secret("FLASK_SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=30)  # Sessions expire after 30 minutes

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/chat", methods=["POST"])
def chat_model():
    session.permanent = True
    LLM_output = "unknown"
    if request.method == "POST":
        if 'conversation' not in session:
            session['conversation'] = [
                {"role": "system", "content": ""},
            ]

        json_data = request.json
        query = json_data.get("query", None)
        if query is None:
            return {"response": "Empty query!"}
        
        session['conversation'].append(
                {"role": "user", "content": f"task: {query}"})
        LLM_output = LLM.create_chat_completion(
            messages=session['conversation'],
            temperature=0.3,
            max_tokens=4096,
            top_k=40,
            repeat_penalty=1.18,
            top_p=0.4,
            min_p=0
            )
        
        response_txt = LLM_output["choices"][0]["message"]["content"]
        session['conversation'].append(
                {"role": "assistant", "content": response_txt})
        session.modified = True
        LLM_output = response_txt

    return {"response": LLM_output}

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    
    return {"status": "logged out"}

@app.route("/workflow", methods=["POST"])
def run_worflow():

    workflow = AgentWorkflow(LLM, grammar)
    workflow.load_data()
    result = workflow.execute()
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
