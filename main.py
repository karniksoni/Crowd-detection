import cv2
from project_utils.detection import load_model, detect_persons
from project_utils.crowd_logic import find_crowds, update_crowd_tracker, log_crowd_events
from config import VIDEO_PATH, DISTANCE_THRESHOLD, FRAME_PERSISTENCE

def main():
    # Load the YOLOv5 model
    model = load_model()

    # Open the video file
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0
    crowd_tracker = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        print(f"Processing frame {frame_count}...")

        # Detect persons in the frame
        persons = detect_persons(model, frame)

        # Find crowds in the current frame
        crowds = find_crowds(persons, DISTANCE_THRESHOLD)

        # Update crowd tracker
        update_crowd_tracker(crowd_tracker, crowds, frame_count)

        # Log crowd events
        log_crowd_events(crowd_tracker, frame_count, FRAME_PERSISTENCE)

        # Optionally, visualize the results
        for person in persons:
            x1, y1, x2, y2, conf, cls = person
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()