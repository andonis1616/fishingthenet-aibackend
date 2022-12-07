from flask import Flask,request,jsonify
from markupsafe import escape

from tensorflow.keras.preprocessing.sequence import pad_sequences
import keras as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle

#Start flask app
app = Flask(__name__)

SEQUENCE_LENGTH = 50 # the length of all sequences (number of words per sample)

def get_predictions(text):
    # tokenizer = Tokenizer()
    sequence = tokenizer.texts_to_sequences([text])
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=SEQUENCE_LENGTH)
    # get the prediction
    prediction = new_model.predict(sequence)
    if prediction >0.50:
        return "Phishing", prediction
    else:
        return "Not Phishing", prediction

fileObj = open('token.tnk', 'rb')
tokenizer = pickle.load(fileObj)
fileObj.close()
new_model = keras.models.load_model('SavedModel.h5')

@app.route('/body', methods=['POST'])
def add_income():
    if request.method == 'POST':
        json = request.get_json()
        isPhishing, percentage = get_predictions(json['content'])
        new_object = {
            "isPhishing" : isPhishing,
            "percentage" : float(percentage[0][0])
        }
        return jsonify(new_object)
    return None