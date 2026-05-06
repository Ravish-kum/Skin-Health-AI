import os

os.environ["HF_HUB_DISABLE_XET"] = "1"

llm_pipeline = None

class DummyPipeline:
    def __init__(self):
        self.tokenizer = DummyTokenizer()
    def __call__(self, *args, **kwargs):
        # Return a dummy response structure similar to pipeline output
        return [{"generated_text": "<|assistant|>Hello! I am your AI Dermatologist. How can I assist you with your diagnosis? (LLM not available)"}]

class DummyTokenizer:
    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True):
        # Simple concatenation of messages for dummy pipeline
        return "".join([msg["content"] for msg in messages])

def get_llm():
    global llm_pipeline
    if llm_pipeline is None:
        try:
            import torch
            from transformers import pipeline
            print("Loading TinyLlama...")
            if torch.cuda.is_available():
                dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
            else:
                dtype = torch.float32

            hf_token = os.environ.get("HF_TOKEN", None)

            llm_pipeline = pipeline(
                "text-generation",
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                dtype=dtype,
                device_map="auto",
                token=hf_token
            )
            print("TinyLlama loaded successfully.")
        except Exception as e:
            # If any error occurs (e.g., tokenizer load failure), fall back to dummy pipeline
            print(f"Failed to load TinyLlama model: {e}. Using dummy pipeline.")
            llm_pipeline = DummyPipeline()
    return llm_pipeline
