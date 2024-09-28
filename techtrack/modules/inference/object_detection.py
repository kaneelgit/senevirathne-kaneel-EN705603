"""
Author - Kaneel Senevirathne
Date - 09/27/2024
An object_detection module that contains a class called Model.
"""
import os
import cv2
import numpy as np

import os, sys
# Add the parent directory (one level up) to the Python path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)


class Model:

    def __init__(self, model_weights_path: str = '../storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.weights',
                 model_config_path: str = '../storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.cfg',
                 names_path: str = '../storage/models/yolo_model_1/logistics.names'):
        """
        Initialize the model given the version
        """ 
        #load model
        self.net = cv2.dnn.readNet(model_weights_path, model_config_path)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def predict(self, preprocessed_frame):

        self.net.setInput(preprocessed_frame)
        outputs = self.net.forward(self.output_layers)
        return outputs

    def post_process(self, predict_output, score_threshold = 0.5):
        
        #get bounding boxes, categories and 
        bounding_boxes = []
        class_categories = []
        scores = []

        for feature_map in predict_output:
            for detection in feature_map:
                boxes = detection[:4]
                score = detection[4]
                class_score = detection[5:]

                #append data if greater than threshold
                if score > score_threshold:
                    bounding_boxes.append(boxes)
                    class_categories.append(np.argmax(class_score))
                    scores.append(score)

        return bounding_boxes, class_categories, scores
    

def draw_bounding_box(image, box, confidence = None, class_id = None, label = None, color=(255, 0, 0), thickness=2):
    """
    Draws a bounding box and label on an image.
    image - numpy array in (x, y, channels) format
    box - tuple with yolo boundary box format (x center, y center, width, height)

    """
        # Ensure the image is in the right format for OpenCV
    image = np.ascontiguousarray(image)
    h, w = image.shape[:2]

    # Get the coordinates from center, width, height (YOLO format)
    cx, cy, bw, bh = box
    x1 = int((cx - bw / 2) * w)
    y1 = int((cy - bh / 2) * h)
    x2 = int((cx + bw / 2) * w)
    y2 = int((cy + bh / 2) * h)

    # Draw bounding box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    if confidence and class_id and label:

        # Add class label and confidence
        label_text = f'{label} {confidence:.2f}'
        cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    return image

def draw_multiple_boxes(image, boxes, confidences=None, class_ids=None, labels=None, color=(255, 0, 0), thickness=2):
    """
    Draws multiple bounding boxes and labels on the same image.
    """
    for i, box in enumerate(boxes):
        confidence = confidences[i] if confidences else None
        class_id = class_ids[i] if class_ids else None
        label = labels[i] if labels else None

        image = draw_bounding_box(image, box, confidence, class_id, label, color, thickness)

    return image