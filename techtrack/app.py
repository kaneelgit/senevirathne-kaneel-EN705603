from modules.inference import preprocessing
from modules.inference import object_detection
from modules.inference import nms
import os
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt

#model path
model_weights_path = 'storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.weights'
model_config_path = 'storage/models/yolo_model_1/yolov4-tiny-logistics_size_416_1.cfg'
names_path = 'storage/models/yolo_model_1/logistics.names'

#save images
save_dir = "storage/prediction/test_1"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

#initialize model
model = object_detection.Model(model_weights_path, model_config_path, names_path)
labels = model.classes

#capture video
for frames in preprocessing.capture_video("udp://127.0.0.1:23000"):

    # print(f"{len(frame)} frames captured")
    for frame in frames:
        predicted_outputs = model.predict(frame)
        bounding_boxes, class_categories, scores = model.post_process(predicted_outputs, score_threshold = 0.25)
        
        #nms
        indices = nms.filter(bounding_boxes, scores, score_threshold=0.0, nms_iou_threshold=0.25)

        filtered_boxes = [bounding_boxes[x] for x in indices]
        filtered_scores = [scores[x] for x in indices]
        filtered_categories = [class_categories[x] for x in indices]  

        filtered_labels = [labels[i] for i in filtered_categories]

        if len(filtered_labels) > 0:

            print(f"Detected objects: {filtered_labels}")

            #frame transposed
            image = np.transpose(frame[0], (1, 2, 0))

            #save frame if an object is there 
            image = object_detection.draw_multiple_boxes(image, filtered_boxes, confidences=filtered_scores, \
                                                 class_ids=filtered_categories , labels=filtered_labels, \
                                                    color=(255, 0, 0), thickness=2)
            
            #save image
            image_name = os.path.join(save_dir, f"{time.time_ns()}.jpg")
            cv2.imwrite(image_name, image * 255.)

            with open(image_name.replace('.jpg', '.txt'), 'w') as file:
                for i, id in enumerate(filtered_categories):
                        #convet to scorer
                        arr = np.zeros(20)
                        arr[id] = filtered_scores[i]
                        for box in filtered_boxes[i]:
                            file.write(f" {box}")
                        file.write(f" {str(filtered_scores[i])}")
                        file.write(" " + " ".join(str(score) for score in arr))
                        file.write(f"\n")
