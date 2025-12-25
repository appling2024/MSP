from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Generator:
    def __init__(self, model_name="google/flan-t5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate_answer(self, question, contexts):
        context = " ".join(contexts)
        prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        output = self.model.generate(**inputs, max_length=128)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
