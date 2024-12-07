# System Report of Moviemate recommendation system

## System Design

### Overview ###
Moviemate is a movie recommendation system that suggests films to users based on ratings data. It consists of three main modules: the adaptive module, the personalization module, and the interface module. The adaptive module supports continuous learning, enabling the system to evolve over time. The recommender system employs a hybrid recommender system consting the collaborative and content based filtering, followed by a diversifier, to recommend movies tailored to individual user preferences. The interface module handles user logins and delivers movie recommendations to the end user.

### Adaptive Module ###
The adaptive module in Moviemate facilitates continuous learning by monitoring the performance of the recommendation model through a statistical evaluation of prediction errors. It uses a baseline dataset of RMSE (Root Mean Squared Error) values, representing the model's initial performance, and compares them against RMSE values generated from new user rating data using a Kolmogorov-Smirnov (KS) test. This test detects distributional drift between the baseline and production data, identifying significant deviations that might indicate model degradation. If the test determines drift, the system flags the need for retraining, allowing the recommendation model to adapt to changing user preferences or new trends in movie ratings. In the moviemate recommendation system, this is set up as a manual endpoint in the docker app to monitor the model performance and retrain if needed. 

### Personalization Module ###
The Personalization module combines a Recommender and a Diversifier to generate and refine item recommendations for users. The Recommender blends content-based and collaborative filtering predictions to rank items based on relevance scores for a given user. It uses a collaborative filtering model, such as SVD, trained on user ratings and metadata to predict user-item scores and produce initial ranked recommendations. Following this, the Diversifier reranks these recommendations by balancing relevance with diversity using customizable diversity measures like intra-list diversity and entropy. It adjusts scores based on a weighted combination of relevance and diversity, ensuring a more diverse yet relevant list of recommendations for the user. Together, these components deliver a hybrid system that prioritizes user-specific preferences while maintaining variety in recommendations.

### Interface Module ###
The interface module provides a seamless way for users to interact with the recommendation system. It includes a method for users to log in and access personalized recommendations based on their preferences and interactions. Additionally, the module supports adding new user information to the database, enabling the system to continuously adapt and include new users. This functionality ensures that both existing and new users can efficiently engage with the system and receive tailored recommendations.

## Metrics Definition

### Offline Metrics ###


### Online Metrics ###


## Analysis of Designing Parameters and Configurations
