import torch

def load_model():
    """
    Load the YOLOv5 model.
    """
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.classes = [0]  # Restrict detection to 'person' class
    return model

def detect_persons(model, frame):
    """
    Detect persons in a frame using the YOLOv5 model.
    """
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # Get detections in (x1, y1, x2, y2, confidence, class) format
    persons = [det for det in detections if int(det[5]) == 0]  # Filter for 'person' class
    return persons