from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
import evaluate
import torch
import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm
from textsummarizer.entity import ModelEvaluationConfig
from textsummarizer.constants import CONFIG_FILE_PATH

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i : i + batch_size]

    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer, batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", column_text="article", column_summary="highlights"):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(zip(article_batches, target_batches), total=len(article_batches)):
            inputs = tokenizer(article_batch, max_length=1024, truncation=True, padding="max_length", return_tensors="pt")
            summaries = model.generate(
                input_ids=inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device),
                length_penalty=0.8, num_beams=8, max_length=128
            )
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True) for s in summaries]
            metric.add_batch(predictions=decoded_summaries, references=target_batch)

        score = metric.compute()
        return score

    def _resolve_path(self, path: Path) -> str:
        candidate = Path(path)
        if candidate.is_absolute():
            return str(candidate)

        project_root = Path(CONFIG_FILE_PATH).resolve().parent.parent
        return str((project_root / candidate).resolve())

    def _normalize_model_dir(self, model_dir: str) -> str:
        resolved_dir = Path(model_dir)
        target_file = resolved_dir / "model.safetensors"

        if target_file.exists():
            return str(resolved_dir)

        shard_files = sorted(resolved_dir.glob("model-*.safetensors"))
        if len(shard_files) == 1:
            shard_files[0].replace(target_file)

        return str(resolved_dir)

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self._resolve_path(self.config.tokenizer_path), local_files_only=True)
        model_dir = self._normalize_model_dir(self._resolve_path(self.config.model_path))
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(model_dir, local_files_only=True).to(device)

        dataset_samsum_pt = load_from_disk(self.config.data_path)

        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        rouge_metric = evaluate.load("rouge")

        score = self.calculate_metric_on_test_ds(dataset_samsum_pt["test"][0:10], rouge_metric, model_pegasus, tokenizer, batch_size=2, column_text="dialogue", column_summary="summary")

        rouge_dict = {
            rn: (score[rn].mid.fmeasure if hasattr(score[rn], "mid") else float(score[rn]))
            for rn in rouge_names
        }

        df = pd.DataFrame(rouge_dict, index=['pegasus'])
        df.to_csv(self.config.metric_file_path, index=False)