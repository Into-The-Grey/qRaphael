import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
MODEL_DIR = "/home/ncacord/qRaphael/models/qRaphael-2b-it"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)


# Define the text generation function
def generate_text(prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        inputs.input_ids, max_length=max_length, num_return_sequences=1, do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example usage
if __name__ == "__main__":
    prompt = "Once upon a time"
    generated_text = generate_text(prompt)
    print(f"Generated text: {generated_text}")
