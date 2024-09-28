"""
Author - Kaneel Senevirathne
Date - 09/27/2024
An object_detection module that contains a class called Model.
"""
import os
import cv2
import numpy as np

class Model:

    def __init__(self, model_weights_path: str = '../../storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.weights',
                 model_config_path: str = '../../storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.cfg',
                 names_path: str = '../../storage/models/yolo_model_1/logistics.names'):
        """
        Initialize the model given the version
        """ 
        #load model
        self.net = cv2.dnn.readNet(model_weights_path, model_config_path)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def predcit(self, preprocessed_frame):

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