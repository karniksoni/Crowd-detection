import numpy as np
from itertools import combinations
from collections import defaultdict

def is_close(box1, box2, threshold):
    """
    Check if two bounding boxes are close to each other.
    """
    center1 = np.array([(box1[0] + box1[2]) / 2, (box1[1] + box1[3]) / 2])
    center2 = np.array([(box2[0] + box2[2]) / 2, (box2[1] + box2[3]) / 2])
    distance = np.linalg.norm(center1 - center2)
    return distance < threshold

def find_crowds(persons, threshold):
    """
    Find groups of 3 or more persons standing close together.
    """
    crowds = []
    for combo in combinations(persons, 3):  # Check all combinations of 3 persons
        if all(is_close(combo[i], combo[j], threshold) for i, j in combinations(range(3), 2)):
            crowds.append(combo)
    return crowds

def update_crowd_tracker(crowd_tracker, crowds, frame_count):
    """
    Update the crowd tracker with detected crowds.
    """
    for crowd in crowds:
        crowd_key = tuple(sorted([tuple(person) for person in crowd]))  # Unique key for each crowd
        crowd_tracker[crowd_key] = crowd_tracker.get(crowd_key, 0) + 1

def log_crowd_events(crowd_tracker, frame_count, persistence):
    """
    Log crowd events that persist for a specified number of frames.
    """
    for crowd_key, duration in list(crowd_tracker.items()):
        if duration >= persistence:
            print(f"Crowd detected at frame {frame_count - duration} to {frame_count}: {crowd_key}")
            # Reset the tracker for this crowd
            del crowd_tracker[crowd_key]