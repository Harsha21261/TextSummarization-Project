import os
from textsummarizer.logging import logger
from transformers import AutoTokenizer
from datasets import load_dataset,load_from_disk
from textsummarizer.entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config:DataTransformationConfig):
        self.config=config
        self.tokenizer_name=AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer_name(example_batch["dialogue"], truncation=True, padding="max_length", max_length=512)
        target_encodings = self.tokenizer_name(example_batch["summary"], truncation=True, padding="max_length", max_length=128)

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    def convert(self):
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt=dataset_samsum.map(self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir,"samsum_dataset"))
