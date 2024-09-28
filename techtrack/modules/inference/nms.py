import cv2
import numpy as np
import time

def filter(boxes, scores, score_threshold=0.0, nms_iou_threshold=0.5):
    """
    Filters bounding boxes using Non-Maximum Suppression (NMS).
    """
    
    # Apply the Non-Maximum Suppression using OpenCV's NMSBoxes
    indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=score_threshold, nms_threshold=nms_iou_threshold)
    
    # Convert the result to a more usable format
    if len(indices) > 0:
        indices = indices.flatten().tolist()  # Convert to a list of indices
    
    return indices