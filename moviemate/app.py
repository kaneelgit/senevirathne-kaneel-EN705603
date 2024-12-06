from flask import Flask, request, jsonify
import pandas as pd
from surprise import SVD
from surprise.model_selection import train_test_split
from surprise import Dataset, Reader, accuracy
import os
from datetime import datetime
from modules.collaborative_filtering import CollaborativeFiltering  # Assuming your class is in `collaborative_filtering.py`
import time

app = Flask(__name__)

# Initialize the recommender system
svd_params = {'n_factors': 200, 'n_epochs': 100, 'lr_all': 0.01, 'reg_all': 0.1}
recommender = CollaborativeFiltering(
    ratings_file='storage/u.data',
    metadata_file='storage/u.item',
    algorithm=SVD(**svd_params)
)
recommender.fit()

@app.route('/add_user', methods=['POST'])
def add_user():
    
    try:
        # Parse JSON payload
        user_data = request.json

        # Extract user information
        age = user_data.get("age")
        gender = user_data.get("gender")
        occupation = user_data.get("occupation")
        zip_code = user_data.get("zip code")
        ratings = user_data.get("ratings", {})

        if not (age and gender and occupation and zip_code):
            return jsonify({"error": "Invalid input. Missing age, gender, occupation, or zip code."}), 400
        
        #USER FILE
        USER_FILE = "storage/u.user"
        USER_COLUMNS = ["user id", "age", "gender", "occupation", "zip code"]

         # Load existing user data
        user_df = pd.read_csv(USER_FILE, sep='|', names=USER_COLUMNS, header=None)

        # Determine the next user ID
        new_user_id = user_df['user id'].max() + 1

        # Add the new user to the dataframe
        new_user_row = pd.DataFrame([[new_user_id, age, gender, occupation, zip_code]], columns=USER_COLUMNS)
        user_df = pd.concat([user_df, new_user_row], ignore_index=True)

        # Save the updated user data back to file
        user_df.to_csv(USER_FILE, sep='|', index=False, header=False)
        
        # If ratings are provided, add them to the u.data file
        DATA_FILE = "storage/u.new_data"
        if ratings:
            data_rows = []
            for item_id, rating in ratings.items():
                timestamp = int(time.time())  # Current Unix timestamp
                data_rows.append(f"{new_user_id}|{item_id}|{rating}|{timestamp}")

            with open(DATA_FILE, 'a') as f:
                f.write('\n'.join(data_rows) + '\n')

        import pdb; pdb.set_trace()
        
        return 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    # Fetch user-specific recommendations
    recommendations = []
    for item_id in recommender.items_metadata['item']:
        prediction = recommender.predict(user_id, item_id)
        recommendations.append((item_id, prediction))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]
    recommended_titles = [
        recommender.items_metadata.loc[recommender.items_metadata['item'] == item_id, 'title'].values[0]
        for item_id, _ in recommendations
    ]
    return jsonify({"recommendations": recommended_titles}), 200

@app.route('/monitor', methods=['POST'])
def monitor():
    retrain = request.get_json().get('retrain', False)
    if retrain:
        recommender._load_data()
        recommender.fit()
        return jsonify({"message": "Model retrained successfully!"}), 200
    return jsonify({"message": "No drift detected."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)