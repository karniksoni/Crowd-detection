
import cv2

def draw_boxes(frame, persons):
    """
    Draw bounding boxes around detected persons.
    """
    for person in persons:
        x1, y1, x2, y2, conf, cls = person
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    return frame