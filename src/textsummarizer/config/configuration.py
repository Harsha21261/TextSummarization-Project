from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from textsummarizer.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from textsummarizer.entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from textsummarizer.utils.common import create_directories, read_yaml


@dataclass
class ConfigurationManager:
    """
    Loads config/params YAML files and builds strongly-typed config objects
    used by the pipeline components.
    """

    config_file_path: Path = CONFIG_FILE_PATH
    params_filepath: Path = PARAMS_FILE_PATH

    def __post_init__(self) -> None:
        self.config = read_yaml(self.config_file_path)
        self.params = read_yaml(self.params_filepath)

        # Create artifacts root if present in config
        artifacts_root = getattr(self.config, "artifacts_root", None)
        if artifacts_root:
            create_directories([artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        cfg = self.config.data_ingestion

        create_directories([cfg.root_dir])

        return DataIngestionConfig(
            root_dir=cfg.root_dir,
            source_url=cfg.source_url,
            local_data_file=cfg.local_data_file,
            unzip_dir=cfg.unzip_dir,
        )
        return self.get_data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config=self.config.data_validation
        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,

        )
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config=self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_name=config.tokenizer_name

        )
        return data_transformation_config
    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config=self.config.model_trainer
        params=self.params.TrainingArgs

        create_directories([config.root_dir])

        model_trainer_config=ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            model_ckpt=config.model_ckpt,
            num_train_epochs=params.num_train_epochs,
            warmup_steps=params.warmup_steps,
            per_device_train_batch_size=params.per_device_train_batch_size,
            weight_decay=params.weight_decay,
            logging_steps=params.logging_steps,
            evaluation_strategy=params.evaluation_strategy,
            eval_steps=params.eval_steps,
            save_steps=params.save_steps,
            gradient_accumulation_steps=params.gradient_accumulation_steps
        )
        return model_trainer_config


    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        project_root = Path(CONFIG_FILE_PATH).resolve().parent.parent

        root_dir = project_root / Path(config.root_dir)
        data_path = project_root / Path(config.data_path)
        model_path = project_root / Path(config.model_path)
        tokenizer_path = project_root / Path(config.tokenizer_path)
        metric_file_path = project_root / Path(config.metric_file_path)

        create_directories([root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=root_dir,
            data_path=data_path,
            model_path=model_path,
            tokenizer_path=tokenizer_path,
            metric_file_path=metric_file_path
        )

        return model_evaluation_config



# Backwards-compatible alias for notebooks/older code
configurationManager = ConfigurationManager


