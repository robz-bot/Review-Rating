from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('wordnet')


reviews =  [{'app':"KFC",'rating': 4, 'comment': "A class above the rest."}, 
            {'app':"PizzaHut",'rating': 3, 'comment': "Absolutely delightful."}, 
            {'app':"Dominos",'rating': 5, 'comment': "Unbeatable quality."}]

app = Flask(__name__)
CORS(app)

# Load dataset from CSV
df = pd.read_csv('reviews.csv')

# Preprocessing
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token not in string.punctuation]
    return ' '.join(tokens)

# Preprocess text data
df['clean_comment'] = df['comment'].apply(preprocess_text)

# Feature extraction
tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X = tfidf_vectorizer.fit_transform(df['clean_comment'])
y = df['label']

# Model training
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X, y)

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json  

    if 'rating' in data and 'comment' in data and 'app' in data:
        rating = data['rating']
        comment = data['comment']
        app_name = data['app']

        # Preprocess the comment and app name
        preprocessed_comment = preprocess_text(comment)
        preprocessed_app_name = preprocess_text(app_name)
        
        # Combine comment and app name
        combined_text = f"{preprocessed_comment} {preprocessed_app_name}"

        # Extract features
        comment_features = tfidf_vectorizer.transform([combined_text])
        
        # Predict using the trained model
        prediction = svm_classifier.predict(comment_features)[0]

        if prediction == 1:
            user_reviews[rating] = {'rating': rating, 'comment': comment, 'app': app_name}
            reviews.append({'rating': rating, 'comment': comment, 'app': app_name})
            # Genuine review
            return jsonify({'status': 'success'})
        else:
            # Fake review detected only if the rating is not extreme (1 or 5)
            if rating != 1 and rating != 5:
                return jsonify({'status': 'error', 'message': 'Fake review detected'}), 400
            else:
                user_reviews[rating] = {'rating': rating, 'comment': comment, 'app': app_name}
                return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing rating, comment, or app name'}), 400


user_reviews={}
@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.json

    email = data['email']
    phoneNumber = data['phoneNumber']

    user_reviews[email] = {'email': email}
    user_reviews[phoneNumber] = {'phoneNumber': phoneNumber}

    return jsonify({'status': 'not_reviewed'})

@app.route('/get_reviews')
def get_reviews():
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True)
