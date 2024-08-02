from flask import Flask
from flask import jsonify
import numpy as np
import time


model = pickle.load(open('house.pkl', 'rb'))

@app.route('/estimate', methods=['POST'])
def predict():
    try:
        int_features = [int(x) for x in request.form.values()]
        features = [np.array(int_features)]
        prediction = model.predict(features)[0]
        formatted_prediction = '{:,.2f}'.format(prediction)
        return jsonify({'prediction_text': 'Your estimated annual rent based on your selected amenities is ₦{}'.format(formatted_prediction)})
        
if __name__ == '__main__':
    app.run(debug=True)
