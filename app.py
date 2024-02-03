# @author Robin Rajesh
# @email robinsiva1998@gmail.com
# @create date 2024-01-24 16:14:58
# @modify date 2024-01-24 16:14:58
# @desc Review and Rating Aggregator Backend code


from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json  

    if 'rating' in data and 'comment' in data:
        rating = data['rating']
        comment = data['comment']

        print(f"Received rating: {rating}")
        print(f"Received comment: {comment}")

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing rating or comment'}), 400

if __name__ == '__main__':
    app.run(debug=True)

