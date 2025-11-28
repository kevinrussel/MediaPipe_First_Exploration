

from typing import Optional
from pathlib import Path
import mediapipe as mp
import json
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
latest_annotated_frame = None


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode



def get_current_milli_time():
    return round(time.time() * 1000)

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



def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    
    global latest_annotated_frame
    
    # Convert mp.Image (RGB) → numpy array
    
    if output_image is None:
        return
    
    annotated_image = output_image.numpy_view().copy()
    latest_annotated_frame = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)



def main(model_path):
    global latest_annotated_frame
    options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
    with GestureRecognizer.create_from_options(options) as recognizer:   
        cam = cv2.VideoCapture(0)
        while True:
            check,frame = cam.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            frame_timestamp_ms = get_current_milli_time()
            recognizer.recognize_async(mp_image, frame_timestamp_ms)

            key = cv2.waitKey(1)
            if key == 27:
                break
            
            if latest_annotated_frame is not None:
                cv2.imshow('video', latest_annotated_frame)
            else:
                cv2.imshow('video',frame)


        cam.release()
        cv2.destroyAllWindows()
        


if __name__ == "__main__":
    model_path = get_model_path()
    main(model_path=model_path)
    print(model_path)