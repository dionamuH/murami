from flask import Flask, request, render_template
from flask import jsonify
import pandas as pd
import pickle
import numpy as np
import time


model = pickle.load(open('house.pkl', 'rb'))

# Mappings for displaying labels
housing_type_mapping = {0: "Duplex", 1: "Flat/Apartment", 2: "Mini Flat", 3: "Selfcon"}
bedroom_mapping = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
bathroom_mapping = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
guest_toilet_mapping = {0: "0", 1: "1", 2: "2", 3: "3"}
parking_space_mapping = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
district_mapping = {
    0: "Abraham Adesanya",1: "Abule Egba",2: "Adeniyi Jones",3: "Agege",4: "Agege-Oko-oba",5: "Ago Palace",6: "Ajah",7: "Ajah-Badore",8: "Alagbado",9: "Alapere",10: "Alimosho",11: "Allen Avenue",12: "Amuwo Odofin",13: "Apapa",14: "Awoyaya",15: "Badagry",16: "Bode Thomas",17: "Ebute Metta",18: "Egbeda",19: "Eko-Atlantic-City",20: "Epe",21: "Festac",22: "Gbagada",23: "Idimu",24: "Ifako",25: "Igando",26: "Iju-Ishaga",27: "Ikeja",28: "Ikeja G.R.A",29: "Ikorodu",30: "Ikotun",31: "Ikoyi",32: "Ilupeju",33: "Isheri",34: "Isheri-Olowora",35: "Isolo",36: "Isolo-Oke-Afa",37: "Iyana Ipaja",38: "Ketu",39: "Kosofe",40: "Lagos Island",41: "Lekki",42: "Lekki Phase 1",43: "Lekki Phase 2",44: "Lekki VGC",45: "Lekki-Admiralty-Way",46: "Lekki-Agungi",47: "Lekki-Chevron",48: "Lekki-Idado",49: "Lekki-Igbo-Efon",50: "Lekki-Ikate",51: "Lekki-Ikota" ,52: "Lekki-Jakande",53: "Lekki-Ologolo",54: "Lekki-Orchid",55: "Lekki-Osapa-London",56: "Magodo",57: "Magodo Phase 2",58: "Maryland",59: "Maryland-Mende",60: "Mushin",61: "Ogba",62: "Ogudu",63: "Ojo",64: "Ojodu Berger",65: "Ojota",66: "Okota",67: "Omole",68: "Omole Phase 2",69: "Onike",70: "Opebi",71: "Opic",72: "Oregun",73: "Oshodi",74: "Oshodi-Ajao",75: "Oshodi-Mafoluku",76: "Sangotedo",77: "Shangisha",78: "Shomolu",79: "Surulere",80: "Victoria Island",81: "Victoria-Island-Oniru",82: "Yaba",83: "Yaba-Akoka",84: "Yaba-Alagomeji"
}


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return (render_template('index.html',
                               housing_type_mapping=housing_type_mapping,
                               bedroom_mapping=bedroom_mapping,
                               bathroom_mapping=bathroom_mapping,
                               guest_toilet_mapping=guest_toilet_mapping,
                               parking_space_mapping=parking_space_mapping,
                               district_mapping=district_mapping))


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