from flask import Flask, request, render_template
from twilio import twiml
from twilio.util import RequestValidator
from twilio.rest import TwilioRestClient
from time import sleep
from threading import Thread

app = Flask(__name__)

@app.route('/phaseOne/', methods=['GET', 'POST'])
def twimlPhonebuzz():

    TOKEN = '4330182d28ec0d81a0f677ebaa5e3f3b'
    validator = RequestValidator(TOKEN)
    url = "http://172.99.78.236/phaseOne/"
    if request.method == 'GET':
        post_variables = {}
    else:
        post_variables = request.form.to_dict()
    sig = request.headers["X-Twilio-Signature"]

    if not validator.validate(url, post_variables, sig) \
        and request.method == 'POST':
        return "Invalid request"

    if request.method == 'POST':
        n = int(request.values.get('Digits', None))
        fizzbuzz = ""
        for i in range (1, n + 1):
            if i % 5 ==0 and i % 3 == 0:
                fizzbuzz += "Fizz Buzz"
            elif i % 3 == 0:
                fizzbuzz += "Fizz"
            elif i % 5 == 0:
                fizzbuzz += "Buzz"
            else:
                fizzbuzz += str(i)
            if (i + 1) <= n:
                fizzbuzz += ", "
        resp = twiml.Response()
        resp.say(fizzbuzz)
        return str(resp)

    elif request.method == 'GET':
        resp = twiml.Response()
        with resp.gather(numDigits=1, action="/phaseOne/", method="POST") as r:
            r.say("Please enter a number")
        return str(resp)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        scheduleThread = Thread(target=scheduleCall,
            args=[request.values.get('phone-number', None),
            int(request.values.get('delay', None)) * 60])

        scheduleThread.start()

        return "Call scheduled"
    elif request.method == 'GET':
        return render_template('index.html')

def scheduleCall(phoneNumber, delay):
    ACCOUNT_SID = "ACe3f2f5b18e73ba630eb75876eeecd76c"
    AUTH_TOKEN = "4330182d28ec0d81a0f677ebaa5e3f3b"

    # Delay for some amount of time
    sleep(delay)
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(
        to=phoneNumber,
        from_="+15594008715",
        url="http://172.99.78.236/phaseOne/",
        method="get",
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
