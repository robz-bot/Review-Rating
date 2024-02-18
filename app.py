# @author Robin Rajesh
# @email robinsiva1998@gmail.com
# @create date 2024-01-24 16:14:58
# @modify date 2024-01-24 16:14:58
# @desc Review and Rating Aggregator Backend code


from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

# Store user reviews in a dictionary (for demonstration purposes)
user_reviews = {}

# New code for checking if the user already reviewed
@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.json

    if 'username' in data and 'email' in data and 'phoneNumber' in data:
        username = data['username']
        email = data['email']
        phoneNumber = data['phoneNumber']

        # Check if the user already reviewed
        if email in user_reviews:
            return jsonify({'status': 'already_reviewed'})
        
        if phoneNumber in user_reviews:
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

        print(f"Received rating: {rating}")
        print(f"Received comment: {comment}")

        user_reviews[rating] = {'rating': rating}
        user_reviews[comment] = {'comment': comment}


        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing rating or comment'}), 400

@app.route('/get_reviews')
def get_reviews():
    reviews_list = [{'rating': 4, 'comment': "Great service!"},{'rating': 3, 'comment': "Good but could be better."}, {'rating': 5, 'comment': "Absolutely fantastic!"}]

    print("66")
    for review in user_reviews:
        reviews_list.append({'rating': review['rating'], 'comment': review['comment']})
    print(reviews_list)    
    return jsonify(reviews_list)

if __name__ == '__main__':
    app.run(debug=True)

