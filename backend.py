from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import json
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   
# Load data

movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

# new_data = pd.read_json('movies_list.json')
# with open('similarity.json', 'r') as f:
#     similarity = np.array(json.load(f))

@app.route('/recommend', methods=['GET'])
def recommend():
    movie = request.args.get('movie')
    try:
        index =movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommendations = [movies.iloc[i[0]].title for i in distances[1:6]]  # Get top 5 recommendations
        return jsonify(recommendations)
    except IndexError:
        return jsonify({"error": "Movie not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)