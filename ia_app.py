
# ia_app.py
from flask import Flask, request, jsonify
import pickle

ia_app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@ia_app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data['keyword']

    # Simuler une recherche pour le moment
    text = " ".join(["dummy text for testing"])  # Remplacer par votre logique de recherche
    text_vectorized = vectorizer.transform([text])
    
    prediction = model.predict(text_vectorized)[0]
    
    return jsonify({'result': prediction})

if __name__ == '__main__':
    ia_app.run(debug=True, host='0.0.0.0', port=5001)

