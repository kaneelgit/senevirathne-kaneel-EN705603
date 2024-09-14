from flask import Flask
import pipeline

app = Flask(__name__)

model_pipeline = pipeline.Pipeline()


@app.route('/')
def home():
<<<<<<< HEAD
    return "hello world"

@app.route('/predict', methods = ["POST"])
def predict():
    global model_pipeline
    data = request.get_json()
    data = model_pipeline.predict(data)
    return data
=======
    return pipeline
>>>>>>> parent of 9f0e296... latest

@app.route('/select_model', methods = ["POST"])
def select_model():
    global model_pipeline
    model_name = request.json.get('model_name')
    model_pipeline = pipeline.Pipeline(model_name)
    return f"Selected model: {model_name}\n"

@app.route('/get_history', methods = ["POST"])
def get_history():
    global model_pipeline    
    history_df = model_pipeline.get_history()
     # Print the DataFrame in a more readable format
    print("Model History DataFrame:")
    print(history_df.to_string(index=False))  # Prints DataFrame without the index
    
    # Return the HTML for the client
    return history_df.to_string(index=False) + '\n'

if __name__ == '__main__':
    app.run(debug=True)
