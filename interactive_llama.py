from llama_cpp import Llama

# Load the model directly from the local file:
llm = Llama(model_path="models/llama-2-7b-chat.Q4_K_M.gguf")

while True:
    user_input = input("\nType your prompt (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    output = llm(f"[INST] {user_input} [/INST]", max_tokens=256, echo=False)
    print(f"\nResponse: {output['choices'][0]['text']}")
