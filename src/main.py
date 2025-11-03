

from typing import Optional
from pathlib import Path
import mediapipe as mp
import json
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def model_path_exists() -> Optional[str]:
    '''
    This function ensures that the path to the config file exists.
    The config file holds the path to the model.
    '''
    base_path = Path.cwd()
    model_path = Path.joinpath(base_path,"config.json")
    if model_path.exists():
        return model_path
    else:
        return None

def get_model_path() -> Optional[str]:
    '''
    Get's the model path from the config file
    Return:
        None -> If the config file doesn't exist
        model_path -> if the config file exists, it gets the path of the model
    '''
    model_path = model_path_exists()
    if not model_path:
        return None
    else:
        with open(model_path, 'r') as file:
            model_file = json.load(file)
        model = model_file["Path_To_Model"]
        return model





if __name__ == "__main__":
    model_path = get_model_path()
    print(model_path)