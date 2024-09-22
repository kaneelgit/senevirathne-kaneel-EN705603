# System Report of SecureBank Fraud Detection System

## System Design

### Overview

The SecureBank Fraud Detection System is a proposed new system designed to effectively identify and prevent fraudulent transactions using machine learning.Packaged within Docker containers, the architecture ensures consistency across various environments and enhances scalability, making it adaptable to the dynamic nature of financial transactions. By leveraging real-time data, the system predicts fraud risks as transactions occur, allowing for immediate action. 

The system requires the following data from a transaction ``` 'trans_date_trans_time', 'cc_num', 'unix_time', 'merchant', 'category', 'amt', 'merch_lat', 'merch_long' ```. Once recieved the system identifies the user and combines the transaction data with the user information to run inference using a selected prexisting model.

### Meeting Requirements

1. **Model Performance -** 
    The proposed system slightly outperforms the older system. The older system reported a precision of 30% and a recall of 60%. The current system includes the best performing model, random forest version 1 with a variable threshold, outperforms the older model with a recall of 34% while maintaining the recall at the same, 60%. 
2. **Generating new datasets -** 
    The proposed system also introduces a method to generate new datasets. This feature generates new train and test sets to perform testing on new models. This is a very useful feature in order to track performance of models.
3. **Selecting a model -** 
    The proposed system has a feature to view performances of currently available pretrained models. This feature shows the recall, precision and the accuracy of each pretrained model so that the administrator can select a suitable model to run inference. Below is an example catelog produced by the system.

```makefile
              Model Version  Precision   Recall  Accuracy
logistic_regression      v1   0.059038 0.730645  0.946855
      random forest      v1   0.121898 0.625806  0.978223
                lda      v1   0.104839 0.650000  0.973683
     sgd_classifier      v1   0.064606 0.745161  0.950740
```
    The system also allows the administrator to select the best model by the model name and version. Once the model is changed, the selected model will be used to run infernece for future transactions.

4. Audit the framework by generating train, test sets from new data sources, and run track performance metrics.

### Unique Functionalities of Developed Modules


### Diagrams


### Summary
The system design incorporates key architectural principles and functionalities to address the requirements for effective fraud detection. The modular structure and real-time processing capabilities position the SecureBank system to adapt to evolving fraud patterns while maintaining high performance and reliability.
