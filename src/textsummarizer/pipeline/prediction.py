from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Use the pre-trained Pegasus model from Hugging Face Hub for quality summaries
MODEL_NAME = "google/pegasus-cnn_dailymail"

class PredictionPipeline:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self._loaded = False

    def _load_model(self):
        """Lazy-load model and tokenizer on first use."""
        if self._loaded:
            return
        
        print(f"Loading pre-trained model: {MODEL_NAME}")
        print("This may take a minute on first run (downloading from Hugging Face)...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(self.device)
        self._loaded = True
        print("Model and tokenizer loaded successfully!")

    def predict(self, text):
        # Load model on first call
        self._load_model()
        
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True).to(self.device)
        
        gen_kwargs = {
            "length_penalty": 0.8, 
            "num_beams": 8, 
            "max_length": 128
        }

        output_tokens = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            **gen_kwargs
        )

        output_text = self.tokenizer.decode(output_tokens[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return output_text
