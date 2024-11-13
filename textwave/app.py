from flask import Flask, request, jsonify, Response
import json
import pipeline
import os


app = Flask(__name__)

@app.route('/query', methods=['POST'])
def upload_json():

    #get data from json file
    data_dict = request.get_json()

    #extract data
    api_key = data_dict["api_key"]
    query = data_dict["query"]
    k = data_dict["k"]

    #initialize pipeline
    pline = pipeline.Pipeline(api_key = api_key)
    query_embedding = pline._encode(query)
    distances_ivf, metadata_ivf = pline.search_neighbors(query_embedding, k)
    query, answer, context = pline.generate_answer(query, metadata_ivf, rerank = True, rerank_type = "hybrid")

    response = f"query: {query}\nanswer: {answer}\n"   

    # Return the response as a JSON
    return response

@app.route('/update_corpus', methods = ["POST"])
def update_corpus():

    file = request.files['file']

    #file path
    file.save(os.path.join('storage', 'corpus', file.filename))

    return "Updated corpus.\n"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)