"""
Author - Kaneel Senevirathne
Date - 09/27/2024
An object_detection module that contains a class called Model.
"""
import os
import cv2
import numpy 

class Model:

    def __init__(self, model_weights_path: str = '../storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.weights',/
                 model_config_path: str = '../storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.cfg'):
        """
        Initialize the model given the version
        """ 
        #load model
        self.net = cv2.dnn.readNet(model_weights_path, model_config_path)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def predcit(self, preprocessed_frame):

        self.net.setInput(preprocessed_frame)
        outputs = self.net.forward(self.output_layers)
        return

    def post_process(self, predict_output, score_threshold = 0.5):

        for feature_map in predict_output:
            for detection in feature_map:
                boxes = detection[:4]
                score = detection[4]
                class_score = detection[5:]