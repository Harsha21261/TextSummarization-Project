from pathlib import Path

# Resolve paths relative to the project root (works even if CWD is different, e.g. notebooks)
_PROJECT_ROOT = Path(__file__).resolve().parents[3]

CONFIG_FILE_PATH = _PROJECT_ROOT / "config" / "config.yaml"
PARAMS_FILE_PATH = _PROJECT_ROOT / "params.yaml"


