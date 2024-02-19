from flask import Flask, request, jsonify
from flask_cors import CORS  
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

# Store user reviews - dataset
user_reviews = {}
reviews =  [{'app': 'KFC' , 'rating': 4, 'comment': "Great service!"}, 
                {'app': 'PizzaHut' ,'rating': 3, 'comment': "Good but could be better."}, 
                {'app': 'Dominos' ,'rating': 5, 'comment': "Absolutely fantastic!"}]

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your SMTP server
app.config['MAIL_PORT'] = 587  # Your SMTP port
app.config['MAIL_USE_TLS'] = True  # Enable TLS
app.config['MAIL_USERNAME'] = 'dummymailrobz@gmail.com'  # Your email username
app.config['MAIL_PASSWORD'] = 'DummyMail@2024'  # Your email password

mail = Mail(app)

# Function to send verification email
@app.route('/send_verification_email', methods=['POST'])
def send_verification_email():
    data = request.json

    if 'email' in data and 'verification_code' in data:
        email = data['email']
        verification_code = data['verification_code']
    msg = Message('Verify Your Email', sender='dummymailrobz@gmail.com', recipients=[email])
    msg.body = f'Your verification code is: {verification_code}'
    print(msg)
    mail.send(msg)

# Dictionary to store email verification codes
verification_codes = {}

@app.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.json
    print(data)
    if 'email' in data and 'verificationCode' in data:
        email = data['email']
        verification_code = data['verificationCode']

        # Check if the verification code matches the one stored for the email
        if email in verification_codes and verification_codes[email] == verification_code:
            # If verification succeeds, remove the verification code from the dictionary
            del verification_codes[email]
            return jsonify({'status': 'verified'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid verification code'}), 400
    else:
        return jsonify({'status': 'error', 'message': 'Missing email or verification code'}), 400

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

        user_reviews[rating] = {'rating': rating}
        user_reviews[comment] = {'comment': comment}
        user_reviews[app] = {'comment': app}

        reviews.append({'rating': int(rating), 'comment': comment, 'app':app})

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing rating or comment'}), 400

@app.route('/get_reviews')
def get_reviews():
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True)
