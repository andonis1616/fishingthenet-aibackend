from flask import Flask,request,jsonify
from markupsafe import escape

from tensorflow.keras.preprocessing.sequence import pad_sequences
import keras as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
import pandas as pd

from tensorflow.keras.layers import Embedding, LSTM, Dropout, Dense, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.metrics import Recall, Precision

#Start flask app
app = Flask(__name__)

SEQUENCE_LENGTH = 50 # the length of all sequences (number of words per sample)

def get_predictions(text):
    sequence = tokenizer.texts_to_sequences([text])
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=SEQUENCE_LENGTH)
    # get the prediction
    prediction = new_model.predict(sequence)
    print(prediction)
    if prediction >0.50:
        return 'Phishing'
    else:
        return 'Not Phishing'

df = pd.read_csv('FINALV1.csv')

df['Body'] = df['Body'].astype(str)

# df = df.sample(frac=1)
# df = df.sample(frac=1)
# df = df.sample(frac=1)

# df_orig = df.copy()

# df['target'] = [1 if x==1 else 0 for  x in df.IsPhishing]
# df.drop('IsPhishing', axis=1, inplace=True)
df.columns = ['from','subject','body','target']
df.drop_duplicates(subset=['body'], keep='first', inplace=True)
# df_Phishing = df[df.target==1]
# df_NoPhishing = df[df.target==0]

X = df.body

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

X = tokenizer.texts_to_sequences(X)

X = pad_sequences(sequences=X, 
                  maxlen=SEQUENCE_LENGTH, 
                  padding='pre', 
                  truncating='post')

new_model = keras.models.load_model('SavedModel.mdl')

print("Emailul 1:")
print(get_predictions("Attention recipient , We have received your request to terminate your email account below, and the request will be concluded within 12hours from now."))

print("Emailul 2:")
print(get_predictions("Welcome Subscriber; Your Annual membership for NORTON 360 TOTAL PROTECTION has been renewed and updated successfully. The amount charged will be reflected within the next 24 to 48 hrs on your profile of account. Product Information: INVOICE NO. @ GGH1644259106OV ITEM NAME @ NORTON 360 TOTAL PROTECTION START DATE @ 2022 Feb 07 END DATE @ 1 year from START DATE GRAND TOTAL @ $240.42 USD PAYMENT METHOD @ Debit from account If you wish to not to continue subscription and claim a REFUND then please feel free to call our Billing Department as soon as possible. You can Reach us on : +1 – ( 803 ) – ( 598 ) – 4473 Regards, Billing Department SP"))

print("Emailul 3:")
print(get_predictions("Hello sir, please let me fix your computer. Click this link"))

print("Emailul 4:")
print(get_predictions("To update your payment method or billing settings, sign in to the Microsoft 365 admin center. \
Sign in to the Office 365 Admin center To Pay Your invoice. \
View this message in the Office 365 Message center \
We hope you're enjoying Subscription For Microsoft 365 E1. Your trial was ended. If you have an Office 365 or Dynamics 365 plan in which Exchange is included, you'll still have access to some email functionality. However, you'll lose access to the full set of Exchange capabilities, including premium connections and features such as Common Data Service. \
Visit our pricing page to learn about Exchange plans."))

@app.route('/body/<id>')
def get_incomes():
    id = escape(id)
    return jsonify(id)


@app.route('/body/<text>', methods=['POST'])
def add_income():
    return jsonify(get_predictions(escape(text)))