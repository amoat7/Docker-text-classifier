from flask import Flask, request, jsonify
import tensorflow as tf
import re
import pandas as pd 
import numpy as np 
import string

@tf.keras.utils.register_keras_serializable()
def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, "<br />", " ")
    line=tf.strings.regex_replace(stripped_html, "[^\x00-\x7F]+", "")
    
    
    return tf.strings.regex_replace(
        line, "[%s]" % re.escape(string.punctuation), ""
    )

model = tf.keras.models.load_model("best_var1")



app = Flask(__name__)


@app.route("/")
def home():
    return "<h3>Text Classification Container</h3>"


@app.route("/predict", methods=["POST"])
def predict():
    payload = pd.DataFrame(request.json)
    prediction = model.predict(payload)
    prediction = np.where(prediction[0][0]>0.5, 'positive', 'negative')
    return jsonify({'prediction':prediction.tolist()})
    
    
if __name__=="__main__":
    app.run(host='0.0.0.0', port=9696, debug=False)