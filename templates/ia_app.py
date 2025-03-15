
# ia_app.py
from flask import Flask, request, jsonify
import pickle
import sqlite3

ia_app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@ia_app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data['keyword']

    # Connexion à la base de données pour rechercher le contenu
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM documents WHERE content LIKE ?", ('%' + keyword + '%',))
    rows = cursor.fetchall()
    conn.close()

    # Créer une liste de résultats
    results = [{'title': row[0], 'content': row[1]} for row in rows]
    return jsonify(results)

if __name__ == '__main__':
    ia_app.run(debug=True, host='0.0.0.0', port=5001)

