# System Report of TechTrack Object Detection System

## System Design

### Overview ###

TechTrack is a computer vision system specifically designed for robotic object detection in warehouse environments. By processing live video feeds, the system accurately identifies key objects such as people, helmets, and safety vests, ensuring both safety and operational efficiency. Leveraging the power of the YOLO model, TechTrack can detect objects from video input and store the data for continuous model improvement through retraining.

The system features an advanced inference pipeline that processes video frames, performs object detection, and applies non-maximal suppression to filter overlapping results. Additionally, TechTrack employs data augmentation and hard negative mining to enhance the model’s performance over time. A set of comprehensive analysis modules evaluates the system's overall effectiveness, providing insights to fine-tune detection accuracy and performance.

Designed with a modular architecture, TechTrack consists of distinct services for inference, interaction, rectification, and analysis. These components work seamlessly to deliver accurate and reliable object detection while maintaining flexibility and scalability for robotic operations in warehouse environments.

![Diagram](diagrams.jpg)

### Inference Service ###

The Inference Service starts with Preprocessing, where frames from the input video are captured, scaled, resized, and prepared for processing. These frames are passed to the Object Detection module, which selects the appropriate model, predicts object classes, applies score thresholds, and draws bounding boxes around detected objects. The NMS (Non-Maximum Suppression) module is then applied to filter overlapping bounding boxes using Intersection-over-Union (IoU) thresholds, ensuring that only the most accurate detections are retained. The results are fed into downstream services for further processing or storage.

### Interface Service ###

The Interface Service facilitates communication between TechTrack and external components. It leverages Docker to manage object detection tasks, including capturing and saving images with detected objects. The system identifies objects such as people, helmets, and safety vests, logging them in real-time and displaying bounding boxes around detected objects in the user interface. The results, including bounding boxes, predicted classes, and probabilities in YOLO format, are saved along with the video frames. This enables both visual inspection of detection outcomes and analytical measurement of model performance, paving the way for future model retraining, particularly with hard negative samples.

### Rectification Service ###

The Rectification Service is dedicated to enhancing the system's detection accuracy. It begins with Augmentation, where various transformations are applied to the input data to create diverse scenarios for model retraining. This process is especially useful for detecting objects in challenging situations, such as during a warehouse fire with heavy smoke, where augmentations help the model learn to detect objects like humans in these adverse conditions. Additionally, Hard Negative Mining identifies difficult false positives or missed detections by calculating the loss and isolating the most challenging examples for the model. These hard negatives are then used to fine-tune the model, improving its performance in handling complex detection cases.

### Analysis Service ###

The Analysis Service assesses the system's overall performance. The Augmentation Analysis module evaluates the impact of various data augmentations on detection accuracy, simulating adverse warehouse scenarios such as mist or smoke that may not naturally occur. This testing environment helps ensure the model can handle unexpected conditions. The Hard Negative Analysis module reviews images flagged through Hard Negative Mining to uncover patterns in the model's errors, providing valuable insights for correction. Finally, the Model Analysis module provides a thorough assessment of the model’s performance, identifying the best-performing versions over time. It also evaluates the speed-accuracy trade-off, ensuring the model is optimized for real-world object detection before deployment.


## Metrics Definition

### Offline Metrics ###

In evaluating our object detection system, offline metrics such as Precision, Recall, and Mean Average Precision (mAP) are critical for understanding the models' performance and guiding improvements. Precision measures the accuracy of positive predictions by calculating the proportion of true positives among all predicted positives, while Recall assesses the models' ability to identify all relevant instances, reflecting the ratio of true positives to total actual positives. Mean Average Precision provides a holistic evaluation by averaging precision across various Intersection over Union (IoU) thresholds, offering deeper insights into detection performance. By leveraging these offline metrics in conjunction with hard negative mining and data augmentation we can identify challenging instances where the models struggle. This targeted approach allows us to retrain the models with these hard negatives and augmented images enhancing their ability to detect objects accurately in complex scenarios. Consequently, the iterative process of assessing offline metrics and refining the training dataset through hard negative mining ensures continuous improvement in detection capabilities, ultimately leading to a more robust object detection system in the warehouse environment.

### Online Metrics ###

For real-time monitoring of our object detection system, online metrics such as the time taken to detect an object in an image are essential to ensure system responsiveness and efficiency. This metric tracks the latency of the detection process, providing insights into how quickly the models can process incoming video frames and generate bounding box predictions. Additionally, we can include metrics such as Frames Per Second (FPS) to evaluate the system's throughput, as well as the success rate of detections over time to ensure consistent performance. Monitoring these online metrics can be achieved through logging and visualization tools that display real-time analytics, allowing for immediate identification of performance bottlenecks and enabling proactive adjustments to maintain optimal operation within the warehouse setting.

## System Parameters and Configurations