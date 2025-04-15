from llama_cpp import Llama

# Load from local file
llm = Llama(model_path="models/llama-2-7b-chat.Q4_K_M.gguf", n_ctx=2048)

# Ask a test prompt
output = llm(
    "### Instruction: Write a good story about a team trying to code a turing tumble game. \n### Response:",
    max_tokens=200
)

print(output["choices"][0]["text"])
