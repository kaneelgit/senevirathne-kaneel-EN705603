"""
Author - Kaneel Senevirathne
Date - 10/05/2024

creating compute loss function and sample hard negative mining data
"""
import cv2
import numpy
import os, sys
import numpy as np

# Add the parent directory (one level up) to the Python path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)

#load the corresponding ground truth bounding box path
def load_annotation(annotation_dir):
    with open(annotation_dir, 'r') as f:
        bboxes = f.readlines()

    #list to capture data
    ground_truth_boxes = []
    classes = []

    #processes the boundary box data
    for bbox in bboxes:
        bbox_split = bbox.split(' ')
        classes.append(int(bbox_split[0]))
        bbox_float = [float(x) for x in bbox_split[1:]]        
        ground_truth_boxes.append(bbox_float)
    
    return ground_truth_boxes, classes


def load_predictions(prediction_dir):

    with open(prediction_dir, 'r') as f:
        bboxes = f.readlines()

    #list to capture data
    ground_truth_boxes = []
    classes = []
    scores = []

    #processes the boundary box data
    for bbox in bboxes:
        bbox_split = bbox.split(' ')
        classes.append(int(bbox_split[0]))
        bbox_float = [float(x) for x in bbox_split[1:5]]        
        ground_truth_boxes.append(bbox_float)
        class_scores = [float(x) for x in bbox_split[5:]]
        scores.append(class_scores)
    
    return ground_truth_boxes, classes, scores


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


#box loss
def box_loss(box_gt, box_pred):    
    box_gt = center_to_corners(box_gt[0], box_gt[1], box_gt[2], box_gt[3])
    box_pred = center_to_corners(box_pred[0], box_pred[1], box_pred[2], box_pred[3])
    loss = (box_gt[0] - box_pred[0])**2 + (box_gt[1] - box_pred[1])**2 + (box_gt[2] - box_pred[2])**2 + (box_gt[3] - box_pred[3])**2
    return loss

def categorical_loss(g_c, p_c):
    #gt array
    gt_arr = np.zeros(20)
    gt_arr[g_c] = 1

    #dot product
    pc_arr = np.array(p_c)
    # Clip the predicted probabilities to avoid log(0)
    pc_arr = np.clip(pc_arr, 1e-15, 1)

    pc_arr = np.log(pc_arr)
    
    return -np.dot(gt_arr, pc_arr)

def objectness_loss(p_0, p_gt_0):
    return (p_0 - p_gt_0)**2

def compute_loss(predictions: list, annotations: list, iou_threshold: float = 0.5):

    #unpack annotations
    boxes_gt = annotations[0]
    classes_gt = annotations[1]

    #predictions
    boxes_pred = predictions[0]
    classes_pred = predictions[1]
    scores_pred = predictions[2]

    #yolo loss
    yolo_loss = 0

    for i, pred_box in enumerate(boxes_pred):
        matched = False #to track if a match was found
        for j, gt_box in enumerate(boxes_gt):
            if calculate_iou(pred_box, gt_box) > iou_threshold:
                box_l = box_loss(pred_box, gt_box)
                cat_l = categorical_loss(classes_gt[j], scores_pred[i])
                obj_l = objectness_loss(scores_pred[i][classes_pred[i]], 1)

                yolo_loss += box_l + cat_l + obj_l
                matched = True
                break

        if not matched: #if the a false positive box
            yolo_loss += objectness_loss(scores_pred[i][classes_pred[i]], 0) #no object detected for prediction

    return yolo_loss

def sample_hard_negatives(prediction_dir: str, annotation_dir: str, num_samples: int, iou_threshold: float = 0.5):

    results_dict = {}

    for i, prediction_path in enumerate(prediction_dir):
        boxes, classes, scores = load_predictions(prediction_path)
        boxes_, classes_ = load_annotation(annotation_dir[i])

        predictions = [boxes, classes, scores]
        annotations = [boxes_, classes_]

        loss = compute_loss(predictions, annotations, iou_threshold = iou_threshold)
        
        #get image dir to put to results
        image_dir = annotation_dir[i].replace('.txt', '.jpg')

        results_dict[image_dir] = (loss, prediction_path, annotation_dir[i])

    # Sort the dictionary by the loss
    sorted_results = sorted(results_dict.items(), key=lambda item: item[1][0], reverse = True)

    return sorted_results[:num_samples]


