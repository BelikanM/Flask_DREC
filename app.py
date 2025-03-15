from flask import Flask, request, jsonify, render_template, send_from_directory, abort
import os
import fitz  # PyMuPDF pour l'extraction de texte
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DATABASE = 'documents.db'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            )
        ''')
        conn.commit()

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def get_relevant_sentences(content, keyword, match_case=False, whole_word=False):
    sentences = content.split('. ')
    relevant_sentences = []

    for sentence in sentences:
        if match_case:
            if whole_word:
                if f' {keyword} ' in sentence:
                    relevant_sentences.append(sentence)
            elif keyword in sentence:
                relevant_sentences.append(sentence)
        else:
            sentence_lower = sentence.lower()
            keyword_lower = keyword.lower()
            if whole_word:
                if f' {keyword_lower} ' in sentence_lower:
                    relevant_sentences.append(sentence)
            elif keyword_lower in sentence_lower:
                relevant_sentences.append(sentence)

    return relevant_sentences

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "Pas de fichier fourni."}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        content = extract_text_from_pdf(file_path)

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO documents (title, content) VALUES (?, ?)", (filename, content))
            conn.commit()

        return jsonify({"message": "Fichier PDF téléchargé et texte extrait avec succès!"})

    return jsonify({"error": "Le fichier n'est pas un PDF valide."}), 400

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    match_case = request.args.get('match_case', 'false').lower() == 'true'
    whole_word = request.args.get('whole_word', 'false').lower() == 'true'

    if not keyword:
        return jsonify([])

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM documents")
        rows = cursor.fetchall()

    results = []
    for title, content in rows:
        relevant_sentences = get_relevant_sentences(content, keyword, match_case, whole_word)

        if relevant_sentences:
            response = ' '.join(relevant_sentences[:10])
            download_link = f'/download/{title}'
            results.append({'title': title, 'content': response, 'download_link': download_link})

    return jsonify(results)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/documents')
def documents():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM documents")
        rows = cursor.fetchall()

    documents = [{'title': row[0], 'download_link': f'/download/{row[0]}'} for row in rows]

    return render_template('documents.html', documents=documents)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
