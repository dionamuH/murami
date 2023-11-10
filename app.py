from flask import Flask, request, render_template
from flask import jsonify
import pandas as pd
import pickle
import numpy as np
import time


model = pickle.load(open('house.pkl', 'rb'))

housing_type_mapping = {0: "Duplex", 1: "Flat/Apartment", 2: "Mini Flat", 3: "Selfcon"}
bedroom_mapping = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
bathroom_mapping = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
guest_toilet_mapping = {0: "0", 1: "1", 2: "2", 3: "3"}
parking_space_mapping = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
district_mapping = {
    0: "Abraham Adesanya",1: "Abule Egba",2: "Adeniyi Jones",3: "Agege",4: "Agege-Oko-oba",...........}


app = Flask(__name__, template_folder='templates', static_folder='static')



@app.route('/estimate', methods=['POST'])
def predict():
    try:
        int_features = [int(x) for x in request.form.values()]
        features = [np.array(int_features)]
        prediction = model.predict(features)[0]
        formatted_prediction = '{:,.2f}'.format(prediction)
        return jsonify({'prediction_text': 'Your estimated annual rent based on your selected amenities is ₦{}'.format(formatted_prediction)})
    except ValueError:
        error_message = 'Oops! Looks like you left something out...Please complete your selection.'
        return jsonify({'error': error_message})
        
if __name__ == '__main__':
    app.run(debug=True)
