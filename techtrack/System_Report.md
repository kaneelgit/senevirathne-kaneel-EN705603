# System Report of SecureBank Fraud Detection System

## System Design

![Diagram](diagrams.jpg)

## Metrics Definition

### Offline Metrics ###

In evaluating our object detection system, offline metrics such as Precision, Recall, and Mean Average Precision (mAP) are critical for understanding the models' performance and guiding improvements. Precision measures the accuracy of positive predictions by calculating the proportion of true positives among all predicted positives, while Recall assesses the models' ability to identify all relevant instances, reflecting the ratio of true positives to total actual positives. Mean Average Precision provides a holistic evaluation by averaging precision across various Intersection over Union (IoU) thresholds, offering deeper insights into detection performance. By leveraging these offline metrics in conjunction with hard negative mining, we can identify challenging instances where the models struggle. This targeted approach allows us to retrain the models with these hard negatives, enhancing their ability to detect objects accurately in complex scenarios. Consequently, the iterative process of assessing offline metrics and refining the training dataset through hard negative mining ensures continuous improvement in detection capabilities, ultimately leading to a more robust object detection system in the warehouse environment.

### Online Metrics ###

For real-time monitoring of our object detection system, online metrics such as the time taken to detect an object in an image are essential to ensure system responsiveness and efficiency. This metric tracks the latency of the detection process, providing insights into how quickly the models can process incoming video frames and generate bounding box predictions. Additionally, we can include metrics such as Frames Per Second (FPS) to evaluate the system's throughput, as well as the success rate of detections over time to ensure consistent performance. Monitoring these online metrics can be achieved through logging and visualization tools that display real-time analytics, allowing for immediate identification of performance bottlenecks and enabling proactive adjustments to maintain optimal operation within the warehouse setting.

## System Parameters and Configurations