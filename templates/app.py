
# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import fitz  # PyMuPDF pour l'extraction de texte
import requests
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        content = extract_text_from_pdf(file_path)
        
        conn = sqlite3.connect('documents.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO documents (title, content) VALUES (?, ?)", (file.filename, content))
        conn.commit()
        conn.close()

        return jsonify({"message": "Fichier PDF téléchargé et texte extrait avec succès!"})
    return jsonify({"error": "Le fichier n'est pas un PDF valide."})

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify([])

    response = requests.post('http://localhost:5001/search', json={'keyword': keyword})

    # Debug: Afficher la réponse de l'API IA
    print("Response from IA API:", response.json())

    results = response.json()
    return jsonify(results)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True, host='0.0.0.0', port=5000)

