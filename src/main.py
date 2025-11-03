

from typing import Optional
from pathlib import Path
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def model_path_exists():
    base_path = Path.cwd()
    model_path = Path.joinpath(base_path,"config.json")

    if model_path.exists():
        return model_path
    else:
        return None

def get_model_path() -> Optional[str]:
    model_path = model_path_exists()
    if not model_path:
        return None
    else:
        return model_path






if __name__ == "__main__":
    model_path = get_model_path()
    print(model_path)