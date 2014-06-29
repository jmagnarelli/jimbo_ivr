import os

from flask import Flask, request

from twilio import twiml

# Declare and configure application
app = Flask(__name__)

@app.route('/ivr')
def test():
    print("got here!")
    return "Howdy, pardner!"

@app.route('/ivr/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    with response.gather(numDigits=1, action="/gather") as gather:
        gather.say("This is only a test. Blaaaaah")
    return str(response)

@app.route('/ivr/gather', methods=['POST'])
def gather():
    response = twiml.Response()
    digits = request.form['Digits']
    if digits == "1":
        response.say("You are correct.  You are the best.")
    else:
        response.say("You are wrong.  Never call me again.")
    return str(response)

# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
