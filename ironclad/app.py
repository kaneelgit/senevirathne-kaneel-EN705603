from flask import Flask, request, jsonify, Response
import numpy as np
from PIL import Image
from retrieval import index
from retrieval import search
import pipeline
import json, os
from datetime import datetime

#flask app
app = Flask(__name__)

def save_search_to_json(k, names):
    file_path = "search_log.json"
    timepoint = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_entry = {
        "timepoint": timepoint,
        "k": k,
        "names": names
    }
    if not os.path.exists(file_path):
        data = []
    else:
        with open(file_path, "r") as file:
            data = json.load(file)
    data.append(search_entry)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

@app.route('/identify', methods = ["POST"])
def identify():
    img = Image.open(request.files['file'])

    findexvgg = index.FaissIndex(faiss_index_type='Flat',  metric='minkowski')
    findexvgg.load(faiss_path = 'storage/catalog_vgg/faiss.index', metadata_path = 'storage/catalog_vgg/metadata.pkl')

    pline2 = pipeline.Pipeline(image_size=160, model_device = 'cpu', pretrained='vggface2')
    pline2.faiss_index = findexvgg

    k = request.form.get('k')

    try:
        k = int(k)
    except:
        k = 5 

    #predict using the model
    out = pline2.search_gallery(img, k = k)

    #predicted names 
    out_names = [o['name'].replace('_', ' ') for o in out]

    #save the names
    save_search_to_json(k, out_names)

    result = "Matched Identities:\n" + '\n'.join(out_names) + '\n'

    return result

@app.route('/history', methods=['GET'])
def history():
    log_file_path = "search_log.json"
    try:
        with open(log_file_path, "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        return "Log file not found!", 404
    
    # Prepare a formatted string for the logs
    formatted_logs = "=== Search Logs ===\n\n"
    for log in logs:
        timepoint = log['timepoint']
        k = log['k']
        names = ', '.join(log['names'])
        formatted_logs += f"Timepoint: {timepoint}\n"
        formatted_logs += f"k: {k}\n"
        formatted_logs += f"Names: {names}\n"
        formatted_logs += "-" * 40 + "\n"  # Separator

    # Return the logs as a plain text response
    return Response(formatted_logs, mimetype='text/plain')

@app.route('/add', methods=['POST'])
def add():
    #load the ucrrent index
    file = request.files['file']
    img = Image.open(file)

    #save file in the catelog
    filename = file.filename
    name = filename.split('.')[0]
    folder_path = os.path.join('storage', 'gallery', name)

    #if dir doesn't exist make dir
    os.makedirs(folder_path, exist_ok = True)

    #define th efull path to save the file
    file_path = os.path.join(folder_path, filename)

    #save image
    img.save(file_path)    

    findexvgg = index.FaissIndex(faiss_index_type='Flat',  metric='minkowski')
    findexvgg.load(faiss_path = 'storage/catalog_vgg/faiss.index', metadata_path = 'storage/catalog_vgg/metadata.pkl')
    pline2 = pipeline.Pipeline(image_size=160, model_device = 'cpu', pretrained='vggface2')
    pline2.faiss_index = findexvgg

    # Compute embedding
    embedding = pline2._encode(img)
    embedding = np.expand_dims(embedding, axis=0) 

    #metadata
    metadata = {"name": name, "image_filename": filename}

    #add embeddingto index
    pline2.faiss_index.add_embeddings(embedding, metadata=metadata)

    #save embedding
    pline2._save_embeddings('storage/catalog_vgg/faiss.index', 'storage/catalog_vgg/metadata.pkl')
    print('Added new person to the gallery and updated the index.')
    return 'Added new person to the gallery and updated the index.\n'

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)
