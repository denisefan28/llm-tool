from flask import Flask, request, session
from llama_cpp import Llama
from datetime import timedelta
from boyfriend import system_prompt


app = Flask(__name__)
LLM = Llama(
    model_path="../models/llama3.2/Llama-3.2-1B-Instruct-Q3_K_XL.gguf",
    chat_format="llama-3",
    return_full_text=True
    )
app.permanent_session_lifetime = timedelta(minutes=30)  # Sessions expire after 30 minutes

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/prompt", methods=["POST"])
def prompt_model():
    session.permanent = True
    LLM_output = "unknown"
    if request.method == "POST":
        if 'conversation' not in session:
            session['conversation'] = [
                {"role": "system", "content": f"{system_prompt}"},
            ]
        json_data = request.json
        query = json_data.get("prompt", "hello")
        
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
    # Method 1: Clear specific key
    #session.pop('conversation', None)
    
    # Method 2: Clear entire session
    session.clear()
    
    # Method 3: Invalidate session
    #session.permanent = False
    
    return {"status": "logged out"}
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
