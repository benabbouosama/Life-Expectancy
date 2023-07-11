import json
import pickle

from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the model and scaler
model = pickle.load(open('MLmodel.pkl', 'rb'))
scaler = pickle.load(open('MLscaling.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output = model.predict(new_data)
    output_json = json.dumps(output[0].tolist())  # Convert ndarray to list and then serialize to JSON
    return jsonify(output_json)

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scaler.transform(np.array(data).reshape(1,-1))
    print(final_input)
    prediction=model.predict(final_input)[0]
    return render_template("index.html", prediction_text="The predicted life expectancy is {} years".format(prediction))

if __name__ == "__main__":
    app.run(debug=True)
