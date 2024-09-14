
import os
import pickle
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV

class train_model():
    """
    Trains a given scikit-learn model, performs hyperparameter tuning if param_grid is provided,
    saves the model to a file, prints the accuracy and classification report, and reloads the saved model.

    """
    def __init__(self, model, X_train, y_train, X_test, y_test, param_grid=None, model_name='model.pkl'):
        
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        
        if param_grid:
            self.param_grid = param_grid

        else:
            self.param_grid = None

        self.model_name = model_name

    def train_model(self):

        # Check if hyperparameters are provided
        if self.param_grid:
            print("Performing hyperparameter tuning with GridSearchCV...")
            grid_search = GridSearchCV(self.model, self.param_grid, cv=5, n_jobs=-1)
            grid_search.fit(self.X_train, self.y_train)
            self.model = grid_search.best_estimator_
            print(f"Best parameters from GridSearchCV: {grid_search.best_params_}")
        
        else:
            # Fit the model with the provided training data
            self.model.fit(self.X_train, self.y_train)

    def predict_(self):
            
        # Predict on the test set
        y_pred = self.model.predict(self.X_test)
        # Print accuracy and classification report
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred)
           
        print(f"Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(report)
        
    def save_model(self):

        # Save the trained model
        with open(self.model_name, 'wb') as file:
            pickle.dump(self.model, file)
        print(f"Model saved as {self.model_name}")

# class load_model()
    
#     # Load the saved model from disk
#     if os.path.exists(model_name):
#         with open(model_name, 'rb') as file:
#             loaded_model = pickle.load(file)
#         print(f"Model {model_name} loaded successfully.")
#     else:
#         raise FileNotFoundError(f"Saved model {model_name} not found!")
    
#     return model, loaded_model

