"""
Author - Kaneel Senevirathne
Date - 10/05/2024

creating compute loss function and sample hard negative mining data
"""
import cv2
import numpy
import os, sys

# Add the parent directory (one level up) to the Python path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)


def center_to_corners(cx, cy, width, height):
    """
    Convert a bounding box from center format (cx, cy, width, height) to
    corner format (x1, y1, x2, y2).
    """
    x1 = cx - width / 2
    y1 = cy - height / 2
    x2 = cx + width / 2
    y2 = cy + height / 2
    return (x1, y1, x2, y2)

def calculate_iou(box1, box2):
    """
    Calculate IoU from bounding boxes given in center format (cx, cy, width, height).
    """
    # Convert center format (cx, cy, w, h) to corner format (x1, y1, x2, y2)
    x1_box1, y1_box1, x2_box1, y2_box1 = center_to_corners(*box1)
    x1_box2, y1_box2, x2_box2, y2_box2 = center_to_corners(*box2)

    # Calculate the coordinates of the intersection rectangle
    x1_inter = max(x1_box1, x1_box2)
    y1_inter = max(y1_box1, y1_box2)
    x2_inter = min(x2_box1, x2_box2)
    y2_inter = min(y2_box1, y2_box2)

    # Calculate the area of the intersection rectangle
    inter_width = max(0, x2_inter - x1_inter)
    inter_height = max(0, y2_inter - y1_inter)
    inter_area = inter_width * inter_height

    # Calculate the area of both bounding boxes
    box1_area = (x2_box1 - x1_box1) * (y2_box1 - y1_box1)
    box2_area = (x2_box2 - x1_box2) * (y2_box2 - y1_box2)

    # Calculate the area of the union (total area minus intersection area)
    union_area = box1_area + box2_area - inter_area

    # Avoid division by zero by ensuring union_area > 0
    if union_area == 0:
        return 0.0

    # Compute the IoU
    iou = inter_area / union_area
    return iou


def compute_loss(prediction: list, annotation: list):
    pass


def sample_hard_negatives(prediction_dir: str, annotation_dir: str, num_samples: int):
    pass



