from flask import Flask, request
from twilio import twiml

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def twimlPhonebuzz():
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
        with resp.gather(numDigits=1, action="/", method="POST") as r:
            r.say("Please enter a number")
        return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
