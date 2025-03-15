
# train.py
import os
import fitz
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_data():
    data = []
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM documents")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'filename': row[0], 'text': row[1]})
    conn.close()
    return data

if __name__ == '__main__':
    data = load_data()
    texts = [d['text'] for d in data]
    labels = [d['filename'] for d in data] 
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2)

    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    model = LogisticRegression()
    model.fit(X_train_vectorized, y_train)

    pickle.dump(model, open('model.pkl', 'wb'))
    pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

