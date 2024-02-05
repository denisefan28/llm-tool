from llama_cpp import Llama

LLM = Llama(model_path="./model/codellama-13b.Q3_K_S.gguf")

prompt = "Q: What is the distance from earth to mars? A:"

output = LLM(prompt)

print(output["choices"][0]["text"])