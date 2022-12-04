from flask import Flask, request, render_template
import numpy as np
import pickle 
app = Flask(__name__)  # initialising flask app

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "oKYwKwwqCY6MmdHMkCDsjwuJoszsHwFfOnN78auQEHTN"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        present_price = float(request.form['price'])
        car_age = int(request.form['age'])
        seller_type = request.form['seller']
        fuel_type = request.form['fuel']
        transmission_type = request.form['transmission']
    

        if fuel_type == 'Diesel':
            fuel_type = 1
        else:
            fuel_type = 0

        if seller_type == 'Individual':
            seller_type = 1
        else:
            seller_type = 0

        if transmission_type == 'Manual':
            transmission_type = 1
        else:
            transmission_type = 0

        res=[present_price, car_age, fuel_type, seller_type, transmission_type]

        # model = pickle.load(open('model', 'rb'))  # load ml model
        payload_scoring = {"input_data": [{"fields": [['Present_Price','Car_age','Fuel_Type_Diesel','Seller_Type_Individual','Transmission_Manual']], "values": [res]}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/49e15694-d946-4b39-b6f4-8e32da7b8c2e/predictions?version=2022-11-18', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        print(response_scoring.json())
        pred=response_scoring.json()
        output=pred['predictions'][0]['values'][0][0]-8
        out=round(output,2)
        print(output)

        return render_template('index.html', output="{} Lakh".format(out))


if __name__ == '__main__':
    app.run(debug=True,port='5003')
