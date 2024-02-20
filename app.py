from flask import Flask, request, jsonify
from flask_cors import CORS  
from flask_mail import Mail, Message
import requests
app = Flask(__name__)
CORS(app)
RECAPTCHA_SECRET_KEY = "6LcSCXkpAAAAAIawZMrR5hhu6ITGhSDqZuZYza99"
# Store user reviews - dataset
user_reviews = {}
reviews =  [{'app': 'KFC' , 'rating': 4, 'comment': "Great service!"}, 
                {'app': 'PizzaHut' ,'rating': 3, 'comment': "Good but could be better."}, 
                {'app': 'Dominos' ,'rating': 5, 'comment': "Absolutely fantastic!"}]

@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.json

    if 'username' in data and 'email' in data and 'phoneNumber' in data:
        email = data['email']
        phoneNumber = data['phoneNumber']

        # Check if the user already reviewed
        if email in user_reviews or phoneNumber in user_reviews:
            return jsonify({'status': 'already_reviewed'})

        # If not reviewed, store the user details for future reference
        user_reviews[email] = {'email': email}
        user_reviews[phoneNumber] = {'phoneNumber': phoneNumber}

        return jsonify({'status': 'not_reviewed'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing username, email, or phoneNumber'}), 400

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json  

    if 'rating' in data and 'comment' in data:
        rating = data['rating']
        comment = data['comment']
        app = data['app']
        recaptcha_response = data['g-recaptcha-response']

        user_reviews[rating] = {'rating': rating}
        user_reviews[comment] = {'comment': comment}
        user_reviews[app] = {'comment': app}

        reviews.append({'rating': int(rating), 'comment': comment, 'app':app})

        # Verify reCAPTCHA response
        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        recaptcha_response = requests.post(recaptcha_verify_url, data=payload)

        if recaptcha_response.status_code == 200:
            recaptcha_data = recaptcha_response.json()
            if recaptcha_data['success']:
                # reCAPTCHA verification successful
                # Proceed with storing the review
                reviews.append({'rating': int(rating), 'comment': comment})
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'reCAPTCHA verification failed'}), 400
        else:
            return jsonify({'status': 'error', 'message': 'Failed to verify reCAPTCHA'}), 500

    else:
        return jsonify({'status': 'error', 'message': 'Missing rating, comment, or reCAPTCHA response'}), 400


@app.route('/get_reviews')
def get_reviews():
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True)
